"""
Gestión de orientaciones (áreas profesionales) desde el panel admin.

- ``nueva_orientacion``     → alta de una orientación para los filtros públicos.
- ``eliminar_orientacion``  → baja de una orientación.
"""

from flask import Blueprint, flash, redirect, request, url_for

from core.decoradores import ajax_o_redirect, requiere_admin
from core.migraciones import asegurar_tabla_orientaciones
from database_handler import obtener_db

bp = Blueprint('admin_orientaciones', __name__)


@bp.route('/admin/orientaciones/nueva', methods=['POST'])
@requiere_admin
def nueva_orientacion():
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la orientación no puede estar vacío.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    asegurar_tabla_orientaciones()
    db = obtener_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO orientaciones (nombre) VALUES (%s)", (nombre,))
        db.commit()
        flash(f'Orientación "{nombre}" agregada. Ya aparece en los filtros de búsqueda.', 'success')
    except Exception:
        db.rollback()
        flash('Esa orientación ya está registrada.', 'warning')
    return redirect(url_for('admin.admin_dashboard'))


@bp.route('/admin/orientaciones/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_orientacion(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM orientaciones WHERE id = %s", (id,))
    db.commit()
    flash('Orientación eliminada.', 'info')
    return redirect(url_for('admin.admin_dashboard'))
