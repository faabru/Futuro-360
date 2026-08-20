"""
Gestión de carreras desde el panel admin (ABM completo).

- ``admin_carreras``   → listado de todas las carreras.
- ``nueva_carrera``    → alta (crea también la tarjeta del juego, inactiva).
- ``editar_carrera``   → modificación de datos y áreas.
- ``eliminar_carrera`` → baja.
"""

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)

from core.decoradores import ajax_o_redirect, requiere_admin
from core.imagenes import guardar_archivo
from core.migraciones import (asegurar_tabla_game_carreras, asegurar_tabla_orientaciones,
                              guardar_areas_carrera, obtener_areas_carrera)
from database_handler import obtener_db

bp = Blueprint('admin_carreras', __name__)


def guardar_imagen_carrera(archivo):
    """Guarda la imagen de una carrera (Cloudinary o local).
    Devuelve la URL/ruta o None si no hay archivo válido."""
    return guardar_archivo(archivo, prefijo='carrera', carpeta='', es_video=False)


def guardar_video_carrera(archivo):
    """Guarda el video de una carrera (Cloudinary o local).
    Devuelve la URL/ruta o None si no hay archivo válido."""
    return guardar_archivo(archivo, prefijo='carrera_video', carpeta='videos',
                           es_video=True)


@bp.route('/admin/carreras')
@requiere_admin
def admin_carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    q = request.args.get('q', '').strip()
    area = request.args.get('area', '').strip()

    where = []
    params = []
    if q:
        where.append("(c.nombre LIKE %s OR c.descripcion LIKE %s)")
        params.extend(['%' + q + '%'] * 2)
    if area:
        where.append(
            "(c.area_profesional = %s OR EXISTS ("
            "SELECT 1 FROM carrera_areas ca WHERE ca.carrera_id = c.id AND ca.area = %s))")
        params.extend([area, area])

    sql = "SELECT c.* FROM carreras c"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY c.nombre"
    cursor.execute(sql, params)
    carreras = cursor.fetchall()

    # Áreas disponibles: orientaciones gestionadas + áreas usadas en carreras.
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT area_profesional FROM carreras WHERE area_profesional <> '' ORDER BY area_profesional")
    areas_carreras = [r['area_profesional'] for r in cursor.fetchall()]
    areas = list(dict.fromkeys(areas_registradas + areas_carreras))

    return render_template('admin/carreras_lista.html', carreras=carreras,
                           areas=areas, q=q, area_actual=area)


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
        if imagen_portada == 'None':
            imagen_portada = ''
        if imagen_principal == 'None':
            imagen_principal = ''
        imagen_portada_subida = guardar_imagen_carrera(request.files.get('imagen_portada_file'))
        imagen_principal_subida = guardar_imagen_carrera(request.files.get('imagen_principal_file'))
        if imagen_portada_subida:
            imagen_portada = imagen_portada_subida
        if imagen_principal_subida:
            imagen_principal = imagen_principal_subida

        # Video: archivo o URL.
        video = request.form.get('video', '')
        if video == 'None':
            video = ''
        video_subido = guardar_video_carrera(request.files.get('video_file'))
        if video_subido:
            video = video_subido

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO carreras (nombre, descripcion, area_profesional, instituciones, imagen_portada, imagen_principal, a_que_se_dedica, video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nombre, descripcion, area_profesional, '', imagen_portada, imagen_principal, a_que_se_dedica, video)
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
        if imagen_portada == 'None':
            imagen_portada = ''
        if imagen_principal == 'None':
            imagen_principal = ''
        imagen_portada_subida = guardar_imagen_carrera(request.files.get('imagen_portada_file'))
        imagen_principal_subida = guardar_imagen_carrera(request.files.get('imagen_principal_file'))
        if imagen_portada_subida:
            imagen_portada = imagen_portada_subida
        if imagen_principal_subida:
            imagen_principal = imagen_principal_subida

        # Video: archivo o URL.
        video = request.form.get('video', '')
        if video == 'None':
            video = ''
        video_subido = guardar_video_carrera(request.files.get('video_file'))
        if video_subido:
            video = video_subido

        cursor.execute(
            "UPDATE carreras SET nombre = %s, descripcion = %s, area_profesional = %s, imagen_portada = %s, imagen_principal = %s, a_que_se_dedica = %s, video = %s WHERE id = %s",
            (nombre, descripcion, area_profesional, imagen_portada, imagen_principal, a_que_se_dedica, video, id)
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
    # Si la carrera solo tiene el área en el campo clásico (sin filas en
    # carrera_areas), la mostramos igual en el dropdown.
    if not areas_carrera and carrera.get('area_profesional'):
        areas_carrera = [carrera['area_profesional']]
    return render_template('admin/carrera_form.html', carrera=carrera,
                           orientaciones=orientaciones, areas_carrera=areas_carrera)


@bp.route('/admin/carreras/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_carrera(id):
    db = obtener_db()
    cursor = db.cursor()
    # Limpiar las áreas vinculadas: carrera_areas no tiene FK a carreras, así
    # que se borran manualmente para no dejar filas huérfanas en el filtro.
    cursor.execute("DELETE FROM carrera_areas WHERE carrera_id = %s", (id,))
    cursor.execute("DELETE FROM carreras WHERE id = %s", (id,))
    db.commit()
    flash('Carrera eliminada exitosamente.', 'info')
    return redirect(url_for('admin_carreras.admin_carreras'))


@bp.route('/admin/carreras/popular/<int:id>', methods=['POST'])
@requiere_admin
def toggle_carrera_popular(id):
    """Marca o desmarca una carrera como 'popular' (destacada en el sitio)."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT popular FROM carreras WHERE id = %s", (id,))
    carrera = cursor.fetchone()
    if not carrera:
        return jsonify(ok=False, error='Carrera no encontrada'), 404
    nuevo = 0 if carrera['popular'] else 1
    cursor.execute("UPDATE carreras SET popular = %s WHERE id = %s", (nuevo, id))
    db.commit()
    return jsonify(ok=True, popular=nuevo)
