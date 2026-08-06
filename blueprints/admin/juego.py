"""
Gestión del mini-juego "Descubre tu Carrera" e "Intereses en Juego" (panel admin).

- ``admin_game_index``       → resumen de carreras y preguntas del juego.
- Carreras: ``admin_game_carreras``, ``toggle_game_carrera``, ``editar_game_carrera``.
- Preguntas: ``admin_game_preguntas``, ``nueva_game_pregunta``,
  ``toggle_game_pregunta``, ``eliminar_game_pregunta``.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.decoradores import ajax_o_redirect, requiere_admin
from core.migraciones import asegurar_columnas_botones_game, asegurar_tabla_orientaciones
from database_handler import obtener_db

bp = Blueprint('admin_juego', __name__)


@bp.route('/admin/game')
@requiere_admin
def admin_game_index():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS n FROM game_carreras WHERE activo = 1")
    carreras_activas = cursor.fetchone()['n']
    cursor.execute("SELECT COUNT(*) AS n FROM game_carreras")
    carreras_total = cursor.fetchone()['n']

    cursor.execute("SELECT COUNT(*) AS n FROM game_preguntas WHERE activo = 1")
    preguntas_activas = cursor.fetchone()['n']
    cursor.execute("SELECT COUNT(*) AS n FROM game_preguntas")
    preguntas_total = cursor.fetchone()['n']

    return render_template('admin/game_index.html',
        carreras_activas=carreras_activas, carreras_total=carreras_total,
        preguntas_activas=preguntas_activas, preguntas_total=preguntas_total)


# --- ADMIN: JUEGO CARRERAS ---

@bp.route('/admin/game/carreras')
@requiere_admin
def admin_game_carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    asegurar_columnas_botones_game(db, cursor)
    cursor.execute("""
        SELECT gc.*, c.nombre as carrera_nombre, c.area_profesional
        FROM game_carreras gc
        JOIN carreras c ON gc.carrera_id = c.id
        ORDER BY gc.orden, c.nombre
    """)
    items = cursor.fetchall()
    return render_template('admin/game_carreras.html', items=items)


@bp.route('/admin/game/carreras/toggle/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def toggle_game_carrera(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE game_carreras SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Estado actualizado en el juego.', 'success')
    return redirect(url_for('admin_juego.admin_game_carreras'))


@bp.route('/admin/game/carreras/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_game_carrera(id):
    texto_boton = request.form.get('texto_boton', 'Ver carrera')
    titulo_card = request.form.get('titulo_card', '')
    descripcion_card = request.form.get('descripcion_card', '')
    boton_no = request.form.get('boton_no', 'No es lo mío')
    boton_info = request.form.get('boton_info', 'Info')
    boton_yes = request.form.get('boton_yes', 'Me interesa')

    db = obtener_db()
    cursor = db.cursor()
    asegurar_columnas_botones_game(db, cursor)
    cursor.execute("""
        UPDATE game_carreras 
        SET texto_boton = %s, titulo_card = %s, descripcion_card = %s,
            boton_no = %s, boton_info = %s, boton_yes = %s
        WHERE id = %s
    """, (texto_boton, titulo_card, descripcion_card, boton_no, boton_info, boton_yes, id))
    db.commit()
    flash('Tarjeta del juego actualizada.', 'success')
    return redirect(url_for('admin_juego.admin_game_carreras'))


# --- ADMIN: INTERESES EN JUEGO (preguntas del mini-juego) ---

@bp.route('/admin/game/preguntas')
@requiere_admin
def admin_game_preguntas():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game_preguntas ORDER BY orden, id")
    preguntas = cursor.fetchall()
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    orientaciones = [o['nombre'] for o in cursor.fetchall()]
    return render_template('admin/game_preguntas.html', preguntas=preguntas, orientaciones=orientaciones)


@bp.route('/admin/game/preguntas/nueva', methods=['POST'])
@requiere_admin
def nueva_game_pregunta():
    texto_pregunta = request.form.get('texto_pregunta', '').strip()
    opcion_a_texto = request.form.get('opcion_a_texto', '').strip()
    opcion_a_area  = request.form.get('opcion_a_area', '').strip()
    opcion_b_texto = request.form.get('opcion_b_texto', '').strip()
    opcion_b_area  = request.form.get('opcion_b_area', '').strip()

    if not all([texto_pregunta, opcion_a_texto, opcion_a_area, opcion_b_texto, opcion_b_area]):
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('admin_juego.admin_game_preguntas'))

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO game_preguntas
        (texto_pregunta, opcion_a_texto, opcion_a_area, opcion_b_texto, opcion_b_area)
        VALUES (%s, %s, %s, %s, %s)
    """, (texto_pregunta, opcion_a_texto, opcion_a_area, opcion_b_texto, opcion_b_area))
    db.commit()
    flash('Pregunta agregada al juego exitosamente.', 'success')
    return redirect(url_for('admin_juego.admin_game_preguntas'))


@bp.route('/admin/game/preguntas/toggle/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def toggle_game_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE game_preguntas SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Estado de la pregunta actualizado.', 'success')
    return redirect(url_for('admin_juego.admin_game_preguntas'))


@bp.route('/admin/game/preguntas/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_game_pregunta(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM game_preguntas WHERE id = %s", (id,))
    db.commit()
    flash('Pregunta eliminada del juego.', 'info')
    return redirect(url_for('admin_juego.admin_game_preguntas'))
