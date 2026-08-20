"""
Gestión de preguntas del test vocacional desde el panel admin.

- ``admin_preguntas``           → listado de preguntas con sus opciones.
- ``nueva_pregunta``            → alta (texto + opciones dinámicas).
- ``eliminar_pregunta``         → baja (las opciones se borran por CASCADE).
- ``eliminar_opcion_pregunta``  → baja de una opción individual.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.decoradores import ajax_o_redirect, requiere_admin
from core.migraciones import asegurar_tabla_orientaciones, registrar_orientaciones
from database_handler import obtener_db

bp = Blueprint('admin_preguntas', __name__)


@bp.route('/admin/preguntas')
@requiere_admin
def admin_preguntas():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM preguntas ORDER BY id")
    preguntas = cursor.fetchall()
    for p in preguntas:
        cursor.execute("SELECT * FROM opciones_pregunta WHERE pregunta_id = %s", (p['id'],))
        p['opciones'] = cursor.fetchall()
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    orientaciones = [o['nombre'] for o in cursor.fetchall()]
    return render_template('admin/preguntas_lista.html', preguntas=preguntas, orientaciones=orientaciones)


@bp.route('/admin/preguntas/nueva', methods=['POST'])
@requiere_admin
def nueva_pregunta():
    texto_pregunta = request.form.get('texto_pregunta', '').strip()
    if not texto_pregunta:
        flash('El texto de la pregunta es obligatorio.', 'danger')
        return redirect(url_for('admin_preguntas.admin_preguntas'))
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO preguntas (texto_pregunta, area_profesional) VALUES (%s, %s)",
                   (texto_pregunta, 'General'))
    pregunta_id = cursor.lastrowid

    # Procesar las opciones enviadas dinámicamente (texto_opcion_N y area_opcion_N).
    i = 1
    areas_nuevas = []
    while f'texto_opcion_{i}' in request.form:
        texto_opcion = request.form.get(f'texto_opcion_{i}', '').strip()
        area_opcion = request.form.get(f'area_opcion_{i}', '').strip()
        if texto_opcion and area_opcion:
            cursor.execute(
                "INSERT INTO opciones_pregunta (pregunta_id, texto_opcion, area_profesional) VALUES (%s, %s, %s)",
                (pregunta_id, texto_opcion, area_opcion)
            )
            # 'Valor nulo' es una opción especial (0 puntos): no es un área real.
            if area_opcion != 'Valor nulo':
                areas_nuevas.append(area_opcion)
        i += 1

    # Registra las áreas escritas a mano para que aparezcan en todos los dropdowns.
    registrar_orientaciones(areas_nuevas)

    db.commit()
    flash('Pregunta agregada con sus opciones exitosamente.', 'success')
    return redirect(url_for('admin_preguntas.admin_preguntas'))


@bp.route('/admin/preguntas/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    # Las opciones se eliminan automáticamente por ON DELETE CASCADE.
    cursor.execute("DELETE FROM preguntas WHERE id = %s", (id,))
    db.commit()
    flash('Pregunta y sus opciones eliminadas.', 'info')
    return redirect(url_for('admin_preguntas.admin_preguntas'))


@bp.route('/admin/preguntas/opcion/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_opcion_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM opciones_pregunta WHERE id = %s", (id,))
    db.commit()
    flash('Opción eliminada.', 'info')
    return redirect(url_for('admin_preguntas.admin_preguntas'))
