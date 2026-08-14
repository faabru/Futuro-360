"""
Gestión de usuarios desde el panel admin (ABM completo: alta, baja, modificación
y activación/desactivación).
"""

import re

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import generate_password_hash

from config import Config
from core.decoradores import ajax_o_redirect, es_usuario_dueño, requiere_admin
from database_handler import obtener_db

bp = Blueprint('admin_usuarios', __name__)


@bp.route('/admin/usuarios')
@requiere_admin
def admin_usuarios():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    total_usuarios = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'admin'")
    total_admins = cursor.fetchone()['total']
    try:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM sesiones_activas "
            "WHERE last_seen >= NOW() - INTERVAL 3 MINUTE")
        total_en_linea = cursor.fetchone()['total']
    except Exception:
        total_en_linea = 0

    f_nombre = request.args.get('nombre', '').strip()
    f_email = request.args.get('email', '').strip()
    f_fecha = request.args.get('fecha', '').strip()
    f_estado = request.args.get('estado', 'todos').strip()

    where = []
    params = []
    if f_nombre:
        where.append("(u.nombre LIKE %s OR u.apellido LIKE %s)")
        params.extend(['%' + f_nombre + '%'] * 2)
    if f_email:
        where.append("u.email LIKE %s")
        params.append('%' + f_email + '%')
    if f_fecha:
        where.append("DATE(u.created_at) = %s")
        params.append(f_fecha)
    if f_estado == 'en_linea':
        where.append("s.last_seen >= NOW() - INTERVAL 3 MINUTE")
    elif f_estado == 'desconectados':
        where.append("(s.last_seen IS NULL OR s.last_seen < NOW() - INTERVAL 3 MINUTE)")

    sql = """SELECT u.id, u.nombre, u.apellido, u.email, u.rol, u.activo, u.created_at,
                    IF(s.last_seen >= NOW() - INTERVAL 3 MINUTE, 1, 0) AS en_linea
             FROM usuarios u
             LEFT JOIN sesiones_activas s ON s.user_id = u.id"""
    if where:
        sql += " WHERE " + " AND ".join(where)
    cursor.execute(sql, params)
    usuarios = cursor.fetchall()

    # Fragmento AJAX: solo la tabla (recargar/filtrar sin refrescar).
    if request.args.get('fragmento') == '1':
        return render_template('admin/_tabla_usuarios.html', usuarios=usuarios,
                               email_dueño=Config.ADMIN_EMAIL,
                               es_dueño=es_usuario_dueño())

    return render_template('admin/usuarios.html', usuarios=usuarios,
                           total_usuarios=total_usuarios, total_admins=total_admins,
                           total_en_linea=total_en_linea,
                           f_nombre=f_nombre, f_email=f_email, f_fecha=f_fecha,
                           f_estado=f_estado,
                           email_dueño=Config.ADMIN_EMAIL,
                           es_dueño=es_usuario_dueño())


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
    # Solo la cuenta principal (dueño) puede crear usuarios.
    if not es_usuario_dueño():
        flash('Solo la cuenta principal puede crear usuarios.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

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
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    if len(password) < 8:
        flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email.strip(),))
    if cursor.fetchone():
        flash('Ya existe un usuario con ese email.', 'warning')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

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
    return redirect(url_for('admin_usuarios.admin_usuarios'))


@bp.route('/admin/usuarios/editar/<int:id>', methods=['POST'])
@requiere_admin
def admin_usuario_editar(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if not usuario:
        flash('El usuario no existe.', 'warning')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    # Solo la cuenta principal (dueño) puede editar usuarios.
    if not es_usuario_dueño():
        flash('Solo la cuenta principal puede editar usuarios.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    nombre = request.form.get('nombre', '')
    apellido = request.form.get('apellido', '')
    email = request.form.get('email', '')
    rol = request.form.get('rol', 'usuario')
    password = request.form.get('password', '')

    error, msg = _validar_usuario_formulario(nombre, apellido, email, rol)
    if error:
        flash(msg, 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    cursor.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (email.strip(), id))
    if cursor.fetchone():
        flash('Ya existe otro usuario con ese email.', 'warning')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    # El dueño del panel no puede ser editado por nadie.
    if usuario.get('es_dueño'):
        flash('La cuenta del dueño del panel no se puede editar.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))
    # Solo el dueño puede modificar el rol/email de otros administradores.
    if usuario.get('rol') == 'admin' and not es_usuario_dueño():
        if rol != 'admin' or email.strip() != usuario['email']:
            flash('Solo el dueño puede modificar el rol o el email de un administrador.', 'danger')
            return redirect(url_for('admin_usuarios.admin_usuarios'))

    try:
        if password:
            if len(password) < 8:
                flash('La contraseña debe tener al menos 8 caracteres.', 'danger')
                return redirect(url_for('admin_usuarios.admin_usuarios'))
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
    return redirect(url_for('admin_usuarios.admin_usuarios'))


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
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    # Solo la cuenta principal (dueño) puede eliminar usuarios.
    if not es_usuario_dueño():
        flash('Solo la cuenta principal puede eliminar usuarios.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    # Evita que el admin se elimine a sí mismo o al dueño del panel.
    if (g.user and usuario['id'] == g.user['id']) or usuario['id'] == session.get('admin_id'):
        flash('No podés eliminar tu propia cuenta desde el panel.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))
    if usuario.get('es_dueño'):
        flash('No podés eliminar al dueño del panel.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))
    # Solo el dueño puede eliminar a otros administradores.
    if usuario.get('rol') == 'admin' and not es_usuario_dueño():
        flash('Solo el dueño puede eliminar administradores.', 'danger')
        return redirect(url_for('admin_usuarios.admin_usuarios'))

    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        db.commit()
        flash('Usuario eliminado correctamente.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error al eliminar el usuario: {e}', 'danger')
    return redirect(url_for('admin_usuarios.admin_usuarios'))


@bp.route('/admin/usuarios/toggle/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def admin_usuario_toggle(id):
    # Pausar o reactivar usuarios está deshabilitado para todos: ni la cuenta
    # principal ni los administradores pueden hacerlo desde el panel.
    flash('No está permitido pausar ni reactivar usuarios desde el panel.', 'danger')
    return redirect(url_for('admin_usuarios.admin_usuarios'))
