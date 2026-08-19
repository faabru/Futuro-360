"""
Rutas de autenticación y perfil del sitio público.

Cubre todo el ciclo de vida de la cuenta del usuario:
- Registro (alta).
- Inicio y cierre de sesión.
- Recuperación de contraseña en 3 pasos (email → código → nueva contraseña).
- Perfil (modificación) y baja de la cuenta (eliminar).
"""

from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import re

import requests

from config import Config
from core.decoradores import requiere_login
from core.seguridad import (minutos_restantes_bloqueo, permite_intento,
                            registrar_exito, registrar_fallo)
from database_handler import obtener_db

# Blueprint del sitio: rutas de autenticación sin prefijo de URL.
bp = Blueprint('auth', __name__)


@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Alta de un nuevo usuario (C de CRUD)."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password_raw = request.form['password']

        if len(password_raw) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('registro.html')

        # Validar formato básico del email (misma regla que el panel admin).
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            flash('El email ingresado no es válido.', 'danger')
            return render_template('registro.html')

        db = obtener_db()
        cursor = db.cursor(dictionary=True)

        # El email es único: se rechaza si ya está registrado.
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('El correo electrónico ya se encuentra registrado.', 'warning')
            return render_template('registro.html')

        password = generate_password_hash(password_raw)

        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password))
            db.commit()

            # Inicia sesión automáticamente tras registrarse.
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            session.clear()
            session['user_id'] = usuario['id']

            flash('¡Registro exitoso! Bienvenido a Futuro 360.', 'success')
            return redirect(url_for('principal.dashboard'))
        except Exception as e:
            db.rollback()
            # No se expone el error interno al usuario (solo se registra en log).
            current_app.logger.error('Error al registrar usuario: %s', e)
            flash('No se pudo completar el registro. Intentá de nuevo.', 'danger')

    return render_template('registro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión con validación de credenciales."""
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        # Anti fuerza bruta: bloquea el email tras varios intentos fallidos.
        if not permite_intento('login', email):
            flash(
                f'Demasiados intentos fallidos. Esperá '
                f'{minutos_restantes_bloqueo("login", email)} minutos e '
                f'intentá de nuevo.',
                'danger')
            return render_template('login.html')

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['password'], password):
            registrar_exito('login', email)
            session.clear()
            session['user_id'] = usuario['id']
            flash(f'¡Qué bueno verte de nuevo, {usuario["nombre"]}!', 'success')
            return redirect(url_for('principal.dashboard'))
        else:
            registrar_fallo('login', email)
            flash('Correo o contraseña incorrectos. Por favor, intenta de nuevo.', 'danger')

    return render_template('login.html')


@bp.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('principal.index'))


@bp.route('/heartbeat', methods=['POST'])
def heartbeat():
    """Ping del navegador: mantiene el estado 'en línea' del usuario mientras
    la pestaña está abierta, aunque no esté navegando. Responde 204 sin cuerpo."""
    id_usuario = session.get('user_id')
    if id_usuario:
        db = obtener_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO sesiones_activas (user_id, last_seen) "
                "VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE last_seen = NOW()",
                (id_usuario,))
            db.commit()
        except Exception:
            try:
                from core.migraciones import asegurar_tabla_sesiones_activas
                asegurar_tabla_sesiones_activas()
                cursor.execute(
                    "INSERT INTO sesiones_activas (user_id, last_seen) "
                    "VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE last_seen = NOW()",
                    (id_usuario,))
                db.commit()
            except Exception:
                pass
    return '', 204


# --- RECUPERACIÓN DE CONTRASEÑA (3 pasos) ---


@bp.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    """PASO 1: el usuario ingresa su email y recibe el código PIN por Resend."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            # El PIN y el envío del correo los genera el servidor Node de
            # recuperación ("recuperacion de contraseña/server.js"), que usa
            # Resend. Acá solo le pedimos el PIN para guardarlo en la BD.
            try:
                resp = requests.post(
                    f"{Config.NODE_RECUPERACION_URL}/recuperar",
                    json={'email': email},
                    timeout=15)
                resp.raise_for_status()
                codigo = str(resp.json().get('pin', ''))
            except Exception as e:
                current_app.logger.error('Error al pedir PIN al server Node: %s', e)
                flash('No se pudo enviar el correo. Intentá de nuevo en unos minutos.', 'danger')
                return render_template('recuperar_password.html')

            if not codigo:
                flash('No se pudo enviar el correo. Intentá de nuevo en unos minutos.', 'danger')
                return render_template('recuperar_password.html')

            # Eliminar códigos anteriores y guardar el nuevo (expira en 15 min).
            # El PIN se guarda HASHEADO (werkzeug): la BD nunca contiene el
            # código en claro, solo su hash. La verificación usa
            # check_password_hash en el paso 2.
            cursor2 = db.cursor()
            cursor2.execute("DELETE FROM password_resets WHERE email = %s", (email,))
            cursor2.execute("""
                INSERT INTO password_resets (email, codigo, expira_en)
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 15 MINUTE))
            """, (email, generate_password_hash(codigo)))
            db.commit()

            flash('✅ Te enviamos un código de 6 dígitos a tu correo. Revisá también spam.', 'success')
        else:
            # Siempre el mismo mensaje por seguridad (no revela emails registrados).
            flash('✅ Si el correo está registrado, recibirás el código en breve.', 'info')

        session['reset_email'] = email
        return redirect(url_for('auth.verificar_codigo'))

    return render_template('recuperar_password.html')


@bp.route('/verificar-codigo', methods=['GET', 'POST'])
def verificar_codigo():
    """PASO 2: el usuario ingresa el código de 6 dígitos recibido por email."""
    email = session.get('reset_email')
    if not email:
        flash('Sesión expirada. Por favor comenzá de nuevo.', 'warning')
        return redirect(url_for('auth.recuperar_password'))

    if request.method == 'POST':
        digitos = [request.form.get(f'd{i}', '') for i in range(1, 7)]
        codigo_ingresado = ''.join(digitos).strip()

        # Anti fuerza bruta: máximo 5 intentos por email y bloqueo de 15 min.
        if not permite_intento('codigo_sitio', email):
            flash(
                f'Demasiados intentos. Esperá '
                f'{minutos_restantes_bloqueo("codigo_sitio", email)} minutos.',
                'danger')
            return render_template('verificar_codigo.html', email=email)

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM password_resets
            WHERE email = %s AND usado = 0 AND expira_en > NOW()
            ORDER BY id DESC LIMIT 1
        """, (email,))
        reset = cursor.fetchone()

        # El PIN se guardó hasheado: se valida con check_password_hash.
        if reset and check_password_hash(reset['codigo'], codigo_ingresado):
            registrar_exito('codigo_sitio', email)
            cursor2 = db.cursor()
            cursor2.execute(
                "UPDATE password_resets SET usado = 1 WHERE id = %s",
                (reset['id'],))
            db.commit()
            session['reset_verificado'] = True
            flash('✅ Código verificado. Ahora podés crear tu nueva contraseña.', 'success')
            return redirect(url_for('auth.nueva_password'))
        else:
            registrar_fallo('codigo_sitio', email)
            flash('❌ Código incorrecto o expirado. Intentá de nuevo o solicitá uno nuevo.', 'danger')

    return render_template('verificar_codigo.html', email=email)


@bp.route('/nueva-password', methods=['GET', 'POST'])
def nueva_password():
    """PASO 3: el usuario define su nueva contraseña."""
    email = session.get('reset_email')
    verificado = session.get('reset_verificado')

    if not email or not verificado:
        flash('Acceso no autorizado. Por favor comenzá de nuevo.', 'warning')
        return redirect(url_for('auth.recuperar_password'))

    if request.method == 'POST':
        password_nueva = request.form.get('password_nueva', '')
        password_confirmar = request.form.get('password_confirmar', '')

        if len(password_nueva) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('nueva_password.html')

        if password_nueva != password_confirmar:
            flash('Las contraseñas no coinciden. Intentá de nuevo.', 'danger')
            return render_template('nueva_password.html')

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET password = %s WHERE email = %s",
            (generate_password_hash(password_nueva), email))
        db.commit()

        session.pop('reset_email', None)
        session.pop('reset_verificado', None)

        flash('🎉 ¡Contraseña actualizada! Ya podés iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('nueva_password.html')


# --- GESTIÓN DE PERFIL (R, U, D de CRUD) ---


@bp.route('/perfil', methods=['GET', 'POST'])
@requiere_login
def perfil():
    """Consulta y modificación de los datos del usuario."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']

        # Validar formato del email (igual que en el registro).
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            flash('El email ingresado no es válido.', 'danger')
            return redirect(url_for('auth.perfil'))

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        # Evita que el usuario ponga un email que ya pertenece a otra cuenta.
        cursor.execute(
            "SELECT id FROM usuarios WHERE email = %s AND id != %s",
            (email, g.user['id']))
        if cursor.fetchone():
            flash('Ese correo ya está en uso por otra cuenta.', 'warning')
            return redirect(url_for('auth.perfil'))
        try:
            cursor.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
                           (nombre, email, g.user['id']))
            db.commit()
            flash('Tu perfil ha sido actualizado correctamente.', 'success')
        except Exception:
            db.rollback()
            flash('No se pudo actualizar el perfil. Intentá de nuevo.', 'danger')
        return redirect(url_for('auth.perfil'))

    return render_template('perfil.html', user=g.user)


@bp.route('/perfil/eliminar', methods=['POST'])
@requiere_login
def eliminar_usuario():
    """Baja definitiva de la cuenta del usuario (D de CRUD)."""
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (g.user['id'],))
    db.commit()
    session.clear()
    flash('Tu cuenta ha sido eliminada. Lamentamos verte partir.', 'info')
    return redirect(url_for('principal.index'))
