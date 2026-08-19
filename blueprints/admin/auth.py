"""
Autenticación del panel de administración.

Login exclusivo (acceso por email de una cuenta con rol admin y activa),
logout y recuperación de contraseña del panel en 3 pasos (igual que el sitio,
pero con correo y plantillas propios).
"""

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from core.decoradores import es_usuario_dueño
from core.migraciones import asegurar_cuenta_dueño
from core.nodo_recuperacion import solicitar_pin
from core.seguridad import (minutos_restantes_bloqueo, permite_intento,
                            registrar_exito, registrar_fallo)
from database_handler import obtener_db

bp = Blueprint('admin_auth', __name__)


@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login independiente para el panel de administración."""
    if session.get('admin_autenticado'):
        return redirect(url_for('admin.admin_dashboard'))

    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '')

        # Anti fuerza bruta: bloquea el email tras varios intentos fallidos.
        if not permite_intento('admin_login', usuario):
            flash(
                f'Demasiados intentos fallidos. Esperá '
                f'{minutos_restantes_bloqueo("admin_login", usuario)} minutos '
                f'e intentá de nuevo.',
                'danger')
            return render_template('admin/login.html')

        asegurar_cuenta_dueño()
        db = obtener_db()
        cursor = db.cursor(dictionary=True)

        # El acceso al panel es solo por email (cuentas con rol admin).
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s AND rol = 'admin' AND activo = 1",
            (usuario,)
        )
        admin = cursor.fetchone()
        if admin and check_password_hash(admin['password'], password):
            registrar_exito('admin_login', usuario)
            session['admin_autenticado'] = True
            session['admin_id'] = admin['id']
            session['admin_nombre'] = f"{admin['nombre']} {admin.get('apellido', '')}".strip()
            session['admin_email'] = admin['email']
            session['admin_es_dueño'] = bool(admin.get('es_dueño'))
            flash('¡Bienvenido al panel de administración!', 'success')
            return redirect(url_for('admin.admin_dashboard'))

        registrar_fallo('admin_login', usuario)
        flash('Email o contraseña incorrectos.', 'danger')

    return render_template('admin/login.html')


@bp.route('/admin/logout')
def admin_logout():
    """Cierra la sesión exclusiva de administración."""
    session.pop('admin_autenticado', None)
    flash('Sesión de administrador cerrada.', 'info')
    return redirect(url_for('admin_auth.admin_login'))


@bp.route('/admin/recuperar-password', methods=['GET', 'POST'])
def admin_recuperar_password():
    """PASO 1: El admin ingresa su correo y recibe el código PIN por Resend."""
    if session.get('admin_autenticado'):
        return redirect(url_for('admin.admin_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        # El código solo se envía si el email pertenece a un admin activo.
        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id FROM usuarios WHERE email = %s AND rol = 'admin' AND activo = 1",
            (email,)
        )
        if cursor.fetchone():
            # El PIN y el envío del correo los genera el servidor Node de
            # recuperación ("recuperacion de contraseña/server.js"), que usa
            # Resend. Si el servidor no está activo, la app lo levanta solo.
            try:
                codigo = solicitar_pin(email)
            except Exception as e:
                current_app.logger.error('Error al pedir PIN al server Node: %s', e)
                flash('No se pudo enviar el correo. Intentá de nuevo en unos minutos.', 'danger')
                return render_template('admin/recuperar_password.html')

            cursor2 = db.cursor()
            cursor2.execute("DELETE FROM password_resets WHERE email = %s", (email,))
            cursor2.execute("""
                INSERT INTO password_resets (email, codigo, expira_en)
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 15 MINUTE))
            """, (email, generate_password_hash(codigo)))
            db.commit()

            flash('✅ Te enviamos un código de 6 dígitos a tu correo. Revisá también spam.', 'success')
        else:
            # Siempre el mismo mensaje por seguridad.
            flash('✅ Si el correo está registrado, recibirás el código en breve.', 'info')

        session['admin_reset_email'] = email
        return redirect(url_for('admin_auth.admin_verificar_codigo'))

    return render_template('admin/recuperar_password.html')


@bp.route('/admin/verificar-codigo', methods=['GET', 'POST'])
def admin_verificar_codigo():
    """PASO 2: El admin ingresa el código de 6 dígitos."""
    email = session.get('admin_reset_email')
    if not email:
        flash('Sesión expirada. Por favor comenzá de nuevo.', 'warning')
        return redirect(url_for('admin_auth.admin_recuperar_password'))

    if request.method == 'POST':
        digitos = [request.form.get(f'd{i}', '') for i in range(1, 7)]
        codigo_ingresado = ''.join(digitos).strip()

        # Anti fuerza bruta: máximo 5 intentos por email y bloqueo de 15 min.
        if not permite_intento('codigo_admin', email):
            flash(
                f'Demasiados intentos. Esperá '
                f'{minutos_restantes_bloqueo("codigo_admin", email)} minutos.',
                'danger')
            return render_template('admin/verificar_codigo.html', email=email)

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
            registrar_exito('codigo_admin', email)
            cursor2 = db.cursor()
            cursor2.execute(
                "UPDATE password_resets SET usado = 1 WHERE id = %s",
                (reset['id'],))
            db.commit()
            session['admin_reset_verificado'] = True
            flash('✅ Código verificado. Ahora podés crear tu nueva contraseña.', 'success')
            return redirect(url_for('admin_auth.admin_nueva_password'))
        else:
            registrar_fallo('codigo_admin', email)
            flash('❌ Código incorrecto o expirado. Intentá de nuevo o solicitá uno nuevo.', 'danger')

    return render_template('admin/verificar_codigo.html', email=email)


@bp.route('/admin/nueva-password', methods=['GET', 'POST'])
def admin_nueva_password():
    """PASO 3: El admin ingresa su nueva contraseña."""
    email = session.get('admin_reset_email')
    verificado = session.get('admin_reset_verificado')

    if not email or not verificado:
        flash('Acceso no autorizado. Por favor comenzá de nuevo.', 'warning')
        return redirect(url_for('admin_auth.admin_recuperar_password'))

    if request.method == 'POST':
        password_nueva = request.form.get('password_nueva', '')
        password_confirmar = request.form.get('password_confirmar', '')

        if len(password_nueva) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
            return render_template('admin/nueva_password.html')

        if password_nueva != password_confirmar:
            flash('Las contraseñas no coinciden. Intentá de nuevo.', 'danger')
            return render_template('admin/nueva_password.html')

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET password = %s WHERE email = %s AND rol = 'admin'",
            (generate_password_hash(password_nueva), email)
        )
        db.commit()

        session.pop('admin_reset_email', None)
        session.pop('admin_reset_verificado', None)

        flash('🎉 ¡Contraseña del panel actualizada! Ya podés iniciar sesión.', 'success')
        return redirect(url_for('admin_auth.admin_login'))

    return render_template('admin/nueva_password.html')
