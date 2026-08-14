"""
Rutas de autenticación y perfil del sitio público.

Cubre todo el ciclo de vida de la cuenta del usuario:
- Registro (alta).
- Inicio y cierre de sesión.
- Recuperación de contraseña en 3 pasos (email → código → nueva contraseña).
- Perfil (modificación) y baja de la cuenta (eliminar).
"""

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from core.decoradores import requiere_login
from core.mailer import enviar_codigo_reset, generar_codigo
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
            flash(f'Error al registrar el usuario: {e}', 'danger')

    return render_template('registro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión con validación de credenciales."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['password'], password):
            session.clear()
            session['user_id'] = usuario['id']
            flash(f'¡Qué bueno verte de nuevo, {usuario["nombre"]}!', 'success')
            return redirect(url_for('principal.dashboard'))
        else:
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
            codigo = generar_codigo()

            # Eliminar códigos anteriores y guardar el nuevo (expira en 15 min).
            cursor2 = db.cursor()
            cursor2.execute("DELETE FROM password_resets WHERE email = %s", (email,))
            cursor2.execute("""
                INSERT INTO password_resets (email, codigo, expira_en)
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 15 MINUTE))
            """, (email, codigo))
            db.commit()

            # Enviar el código por correo.
            try:
                enviar_codigo_reset(email, codigo)
                flash('✅ Te enviamos un código de 6 dígitos a tu correo. Revisá también spam.', 'success')
            except Exception as e:
                flash(f'Error al enviar el email: {str(e)}', 'danger')
                return render_template('recuperar_password.html')
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

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM password_resets
            WHERE email = %s AND codigo = %s AND usado = 0 AND expira_en > NOW()
        """, (email, codigo_ingresado))
        reset = cursor.fetchone()

        if reset:
            cursor2 = db.cursor()
            cursor2.execute(
                "UPDATE password_resets SET usado = 1 WHERE id = %s",
                (reset['id'],))
            db.commit()
            session['reset_verificado'] = True
            flash('✅ Código verificado. Ahora podés crear tu nueva contraseña.', 'success')
            return redirect(url_for('auth.nueva_password'))
        else:
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

        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
                       (nombre, email, g.user['id']))
        db.commit()
        flash('Tu perfil ha sido actualizado correctamente.', 'success')
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
