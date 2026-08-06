"""
Gestión de usuarios desde el panel admin (ABM completo: alta, baja, modificación
y activación/desactivación).
"""

import re

from flask import (Blueprint, flash, g, redirect, request, session, url_for)
from werkzeug.security import generate_password_hash

from core.decoradores import ajax_o_redirect, es_usuario_dueño, requiere_admin
from database_handler import obtener_db

bp = Blueprint('admin_usuarios', __name__)


def _validar_usuario_formulario(nombre, apellido, email, rol):
    """Valida los campos del formulario de usuario. Devuelve (error, msg)."""
    nombre = (nombre or '').strip()
    email = (email or '').strip()
    if not nombre:
        return True, 'El nombre es obligatorio.'
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return True, 'El email ingresado no es válido.'
    if rol not in ('usuario', 'admin'):
        return True, 'El rol seleccionado no es válido.'
    return False, ''


@bp.route('/admin/usuarios/nuevo', methods=['POST'])
@requiere_admin
def admin_usuario_nuevo():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    nombre = request.form.get('nombre', '')
    apellido = request.form.get('apellido', '')
    email = request.form.get('email', '')
    rol = request.form.get('rol', 'usuario')
    password = request.form.get('password', '')

    error, msg = _validar_usuario_formulario(nombre, apellido, email, rol)
    if error:
        flash(msg, 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    if len(password) < 8:
        flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email.strip(),))
    if cursor.fetchone():
        flash('Ya existe un usuario con ese email.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido, email, password, rol) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellido.strip(), email.strip(), password_hash, rol))
        db.commit()
        flash('Usuario creado correctamente.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error al crear el usuario: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))


@bp.route('/admin/usuarios/editar/<int:id>', methods=['POST'])
@requiere_admin
def admin_usuario_editar(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if not usuario:
        flash('El usuario no existe.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    nombre = request.form.get('nombre', '')
    apellido = request.form.get('apellido', '')
    email = request.form.get('email', '')
    rol = request.form.get('rol', 'usuario')
    password = request.form.get('password', '')

    error, msg = _validar_usuario_formulario(nombre, apellido, email, rol)
    if error:
        flash(msg, 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email.strip(), id))
    if cursor.fetchone():
        flash('Ya existe otro usuario con ese email.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    # El dueño del panel no puede ser editado por nadie.
    if usuario.get('es_dueño'):
        flash('La cuenta del dueño del panel no se puede editar.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    # Solo el dueño puede modificar el rol/email de otros administradores.
    if usuario.get('rol') == 'admin' and not es_usuario_dueño():
        if rol != 'admin' or email.strip() != usuario['email']:
            flash('Solo el dueño puede modificar el rol o el email de un administrador.', 'danger')
            return redirect(url_for('admin.admin_dashboard'))

    try:
        if password:
            if len(password) < 8:
                flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
                return redirect(url_for('admin.admin_dashboard'))
            password_hash = generate_password_hash(password)
            cursor.execute(
                "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, rol = %s, password = %s WHERE id = %s",
                (nombre, apellido.strip(), email.strip(), rol, password_hash, id))
        else:
            cursor.execute(
                "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, rol = %s WHERE id = %s",
                (nombre, apellido.strip(), email.strip(), rol, id))
        db.commit()
        flash('Usuario actualizado correctamente.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error al actualizar el usuario: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))


@bp.route('/admin/usuarios/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def admin_usuario_eliminar(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if not usuario:
        flash('El usuario no existe.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    # Evita que el admin se elimine a sí mismo o al dueño del panel.
    if (g.user and usuario['id'] == g.user['id']) or usuario['id'] == session.get('admin_id'):
        flash('No podés eliminar tu propia cuenta desde el panel.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    if usuario.get('es_dueño'):
        flash('No podés eliminar al dueño del panel.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    # Solo el dueño puede eliminar a otros administradores.
    if usuario.get('rol') == 'admin' and not es_usuario_dueño():
        flash('Solo el dueño puede eliminar administradores.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        db.commit()
        flash('Usuario eliminado correctamente.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error al eliminar el usuario: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))


@bp.route('/admin/usuarios/toggle/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def admin_usuario_toggle(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if not usuario:
        flash('El usuario no existe.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    if (g.user and usuario['id'] == g.user['id']) or usuario['id'] == session.get('admin_id'):
        flash('No podés desactivar tu propia cuenta.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    if usuario.get('es_dueño'):
        flash('No podés desactivar al dueño del panel.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    # Solo el dueño puede desactivar a otros administradores.
    if usuario.get('rol') == 'admin' and not es_usuario_dueño():
        flash('Solo el dueño puede desactivar administradores.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    nuevo_estado = 0 if usuario.get('activo') else 1
    cursor.execute("UPDATE usuarios SET activo = %s WHERE id = %s", (nuevo_estado, id))
    db.commit()
    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
