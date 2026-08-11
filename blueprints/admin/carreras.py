"""
Gestión de carreras desde el panel admin (ABM completo).

- ``admin_carreras``   → listado de todas las carreras.
- ``nueva_carrera``    → alta (crea también la tarjeta del juego, inactiva).
- ``editar_carrera``   → modificación de datos y áreas.
- ``eliminar_carrera`` → baja.
"""

import os
import time

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from werkzeug.utils import secure_filename

from config import EXTENSIONES_IMAGEN
from core.decoradores import ajax_o_redirect, requiere_admin
from core.migraciones import (asegurar_tabla_game_carreras, asegurar_tabla_orientaciones,
                              guardar_areas_carrera, obtener_areas_carrera)
from database_handler import obtener_db

bp = Blueprint('admin_carreras', __name__)


def guardar_imagen_carrera(archivo):
    """Guarda una imagen subida desde el formulario en static/imagenes/.
    Devuelve la ruta relativa 'imagenes/<nombre>' o None si no hay archivo válido."""
    if archivo is None or not archivo.filename:
        return None

    nombre_original = secure_filename(archivo.filename)
    if not nombre_original:
        return None

    ext = nombre_original.rsplit('.', 1)[-1].lower() if '.' in nombre_original else ''
    if ext not in EXTENSIONES_IMAGEN:
        return None

    # Nombre único para evitar colisiones (prefijo con timestamp).
    nombre = f"carrera_{int(time.time())}_{nombre_original}"
    ruta = os.path.join(current_app.static_folder, 'imagenes', nombre)
    archivo.save(ruta)
    return f"imagenes/{nombre}"


@bp.route('/admin/carreras')
@requiere_admin
def admin_carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras")
    carreras = cursor.fetchall()
    return render_template('admin/carreras_lista.html', carreras=carreras)


@bp.route('/admin/carreras/nueva', methods=['GET', 'POST'])
@requiere_admin
def nueva_carrera():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        descripcion = request.form.get('descripcion', '')
        areas = request.form.getlist('area_profesional')
        areas = [a.strip() for a in areas if a and a.strip()]
        area_profesional = areas[0] if areas else ''
        a_que_se_dedica = request.form.get('a_que_se_dedica', '')

        # Imágenes: si se sube un archivo, se usa en lugar de la URL.
        imagen_portada = request.form.get('imagen_portada', '')
        imagen_principal = request.form.get('imagen_principal', '')
        imagen_portada_subida = guardar_imagen_carrera(request.files.get('imagen_portada_file'))
        imagen_principal_subida = guardar_imagen_carrera(request.files.get('imagen_principal_file'))
        if imagen_portada_subida:
            imagen_portada = imagen_portada_subida
        if imagen_principal_subida:
            imagen_principal = imagen_principal_subida

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO carreras (nombre, descripcion, area_profesional, instituciones, imagen_portada, imagen_principal, a_que_se_dedica) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nombre, descripcion, area_profesional, '', imagen_portada, imagen_principal, a_que_se_dedica)
        )
        carrera_id_nueva = cursor.lastrowid
        db.commit()
        # Registra la carrera nueva en el juego "Descubre tu carrera" (inactiva
        # por defecto, el admin la activa desde el panel). También crea la tabla
        # si no existe y agrega cualquier carrera que falte.
        asegurar_tabla_game_carreras()
        guardar_areas_carrera(carrera_id_nueva, areas)
        flash('Carrera creada. Las instituciones se completarán con el buscador web en el detalle de la carrera.', 'success')
        return redirect(url_for('admin_carreras.admin_carreras'))

    asegurar_tabla_orientaciones()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    orientaciones = [r['nombre'] for r in cursor.fetchall()]
    return render_template('admin/carrera_form.html', carrera=None,
                           orientaciones=orientaciones, areas_carrera=[])


@bp.route('/admin/carreras/editar/<int:id>', methods=['GET', 'POST'])
@requiere_admin
def editar_carrera(id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        descripcion = request.form.get('descripcion', '')
        areas = request.form.getlist('area_profesional')
        areas = [a.strip() for a in areas if a and a.strip()]
        area_profesional = areas[0] if areas else ''
        a_que_se_dedica = request.form.get('a_que_se_dedica', '')

        # Imágenes: si se sube un archivo, se usa en lugar de la URL.
        imagen_portada = request.form.get('imagen_portada', '')
        imagen_principal = request.form.get('imagen_principal', '')
        imagen_portada_subida = guardar_imagen_carrera(request.files.get('imagen_portada_file'))
        imagen_principal_subida = guardar_imagen_carrera(request.files.get('imagen_principal_file'))
        if imagen_portada_subida:
            imagen_portada = imagen_portada_subida
        if imagen_principal_subida:
            imagen_principal = imagen_principal_subida

        cursor.execute(
            "UPDATE carreras SET nombre = %s, descripcion = %s, area_profesional = %s, imagen_portada = %s, imagen_principal = %s, a_que_se_dedica = %s WHERE id = %s",
            (nombre, descripcion, area_profesional, imagen_portada, imagen_principal, a_que_se_dedica, id)
        )
        db.commit()
        # Asegura que la carrera editada siga vinculada al juego.
        asegurar_tabla_game_carreras()
        guardar_areas_carrera(id, areas)
        flash('Carrera actualizada exitosamente.', 'success')
        return redirect(url_for('admin_carreras.admin_carreras'))

    cursor.execute("SELECT * FROM carreras WHERE id = %s", (id,))
    carrera = cursor.fetchone()
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    orientaciones = [r['nombre'] for r in cursor.fetchall()]
    areas_carrera = obtener_areas_carrera(id)
    return render_template('admin/carrera_form.html', carrera=carrera,
                           orientaciones=orientaciones, areas_carrera=areas_carrera)


@bp.route('/admin/carreras/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_carrera(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM carreras WHERE id = %s", (id,))
    db.commit()
    flash('Carrera eliminada exitosamente.', 'info')
    return redirect(url_for('admin_carreras.admin_carreras'))
