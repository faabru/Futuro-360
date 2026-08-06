"""
Rutas del mini-juego "Descubre tu Carrera" e "Intereses en Juego".

- ``juego`` → pantalla del juego interactivo con las carreras y preguntas
              activas, serializadas en JSON para el frontend.
"""

import json

from flask import Blueprint, render_template

from core.decoradores import requiere_login
from core.migraciones import asegurar_columnas_botones_game
from database_handler import obtener_db

bp = Blueprint('juegos', __name__)


@bp.route('/juego')
@requiere_login
def juego():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Asegura las columnas de los botones en game_carreras.
    asegurar_columnas_botones_game(db, cursor)

    # Carreras activas en el juego.
    cursor.execute("""
        SELECT gc.*, c.nombre as carrera_nombre, c.id as carrera_id, c.area_profesional,
               c.descripcion as carrera_descripcion, c.a_que_se_dedica as carrera_dedica
        FROM game_carreras gc
        JOIN carreras c ON gc.carrera_id = c.id
        WHERE gc.activo = 1
        ORDER BY gc.orden
    """)
    carreras_juego = cursor.fetchall()

    # Preguntas activas del mini-juego "Intereses en Juego".
    cursor.execute("""
        SELECT * FROM game_preguntas
        WHERE activo = 1
        ORDER BY orden, id
    """)
    game_preguntas = cursor.fetchall()

    carreras_json = json.dumps(
        [{'id': r['carrera_id'], 'nombre': r['carrera_nombre'],
          'area_profesional': r['area_profesional'],
          'descripcion': r['descripcion_card'] or '',
          'descripcion_completa': r['carrera_descripcion'] or '',
          'a_que_se_dedica': r['carrera_dedica'] or '',
          'titulo_card': r['titulo_card'] or r['carrera_nombre'],
          'texto_boton': r['texto_boton'] or 'Ver carrera',
          'boton_no': r.get('boton_no') or 'No es lo mío',
          'boton_info': r.get('boton_info') or 'Info',
          'boton_yes': r.get('boton_yes') or 'Me interesa'} for r in carreras_juego],
        ensure_ascii=False
    )

    preguntas_json = json.dumps(
        [{'id': p['id'],
          'texto': p['texto_pregunta'],
          'opciones': [
              {'texto': p['opcion_a_texto'], 'area': p['opcion_a_area']},
              {'texto': p['opcion_b_texto'], 'area': p['opcion_b_area']}
          ]} for p in game_preguntas],
        ensure_ascii=False
    )

    return render_template('juego.html',
        carreras_json=carreras_json,
        carreras_juego=carreras_juego,
        preguntas_json=preguntas_json,
        game_preguntas=game_preguntas
    )
