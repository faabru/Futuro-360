"""
Gestión de noticias, fuentes y filtros de fecha desde el panel admin.

- ``admin_noticias``   → listado con filtros y buscador.
- Noticias: ``nueva_noticia``, ``editar_noticia``, ``eliminar_noticia``.
- Fuentes: ``nueva_fuente``, ``editar_fuente``, ``toggle_fuente``,
  ``eliminar_fuente`` (con tabla de eliminadas para no auto-registrarlas).
- Filtros de fecha: ``nueva_filtro_fecha``, ``editar_filtro_fecha``,
  ``mover_filtro_fecha``, ``eliminar_filtro_fecha``.
"""

import re
from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template,
                   request, url_for)

from core.decoradores import ajax_o_redirect, requiere_admin
from core.imagenes import guardar_archivo
from core.migraciones import (asegurar_tabla_filtros_fecha, asegurar_tabla_fuentes,
                              asegurar_tabla_orientaciones, registrar_orientaciones)
from database_handler import obtener_db

bp = Blueprint('admin_noticias', __name__)


def guardar_imagen_noticia(archivo):
    """Guarda la imagen de una noticia (Cloudinary o local).
    Devuelve la URL/ruta o None si no hay archivo válido."""
    return guardar_archivo(archivo, prefijo='noticia', carpeta='noticias',
                           es_video=False)


def guardar_video_noticia(archivo):
    """Guarda el video de una noticia (Cloudinary o local).
    Devuelve la URL/ruta o None si no hay archivo válido."""
    return guardar_archivo(archivo, prefijo='noticia_video', carpeta='videos',
                           es_video=True)


@bp.route('/admin/noticias')
@requiere_admin
def admin_noticias():
    asegurar_tabla_fuentes()
    asegurar_tabla_filtros_fecha()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    filtro_fecha = request.args.get('fecha', 'todas')
    filtro_fuente = request.args.get('fuente', 'todas')
    filtro_categoria = request.args.get('categoria', 'todas')
    busqueda = request.args.get('q', '').strip()

    # Filtros de búsqueda.
    query = "SELECT * FROM noticias WHERE 1=1"
    params = []

    # Filtro por fecha: usa la condición guardada en la tabla filtros_fecha.
    if filtro_fecha != 'todas':
        cursor.execute("SELECT condicion FROM filtros_fecha WHERE valor = %s", (filtro_fecha,))
        fila_fecha = cursor.fetchone()
        if fila_fecha and fila_fecha['condicion']:
            query += " AND " + fila_fecha['condicion']

    if filtro_fuente != 'todas':
        query += " AND fuente = %s"
        params.append(filtro_fuente)

    if filtro_categoria != 'todas':
        query += " AND categoria = %s"
        params.append(filtro_categoria)

    if busqueda:
        query += " AND (titulo LIKE %s OR descripcion LIKE %s OR fuente LIKE %s)"
        params.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"])

    query += " ORDER BY fecha DESC, id DESC"
    cursor.execute(query, params)
    noticias = cursor.fetchall()

    # Fuentes: registradas en la tabla + las existentes en noticias (sin las eliminadas).
    cursor.execute("SELECT DISTINCT fuente FROM noticias ORDER BY fuente")
    fuentes_noticias = [r['fuente'] for r in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes ORDER BY nombre")
    fuentes_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes_eliminadas")
    fuentes_eliminadas = [r['nombre'] for r in cursor.fetchall()]
    fuentes = list(dict.fromkeys(
        fuentes_registradas + [f for f in fuentes_noticias if f not in fuentes_eliminadas]
    ))

    # Categorías: orientaciones registradas + las existentes en noticias.
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT categoria FROM noticias ORDER BY categoria")
    categorias_noticias = [r['categoria'] for r in cursor.fetchall()]
    categorias = list(dict.fromkeys(areas_registradas + categorias_noticias))

    # Dropdown del formulario: orientaciones + áreas profesionales de las carreras.
    cursor.execute("""
        SELECT DISTINCT area_profesional FROM carreras
        WHERE area_profesional IS NOT NULL AND area_profesional <> ''
        ORDER BY area_profesional
    """)
    areas_carreras = [r['area_profesional'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT area FROM carrera_areas ORDER BY area")
    areas_carrera_areas = [r['area'] for r in cursor.fetchall()]
    areas_dropdown = list(dict.fromkeys(
        ['General'] + areas_registradas + areas_carreras + areas_carrera_areas + categorias_noticias
    ))

    cursor.execute("SELECT * FROM fuentes ORDER BY nombre")
    fuentes_tabla = cursor.fetchall()

    cursor.execute("SELECT * FROM filtros_fecha ORDER BY orden, id")
    filtros_fecha = cursor.fetchall()

    return render_template('admin/noticias_lista.html',
        noticias=noticias, fuentes=fuentes, categorias=categorias,
        areas_dropdown=areas_dropdown,
        fuentes_tabla=fuentes_tabla, filtros_fecha=filtros_fecha,
        filtro_fecha=filtro_fecha, filtro_fuente=filtro_fuente,
        filtro_categoria=filtro_categoria, busqueda=busqueda)


@bp.route('/admin/noticias/nueva', methods=['POST'])
@requiere_admin
def nueva_noticia():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    fuente = request.form['fuente']
    fecha = request.form['fecha']
    link = request.form.get('link', '#')
    categoria = request.form.get('categoria', 'General')

    # Imagen: si se sube un archivo, se usa en lugar de la URL.
    imagen = request.form.get('imagen', '')
    imagen_subida = guardar_imagen_noticia(request.files.get('imagen_file'))
    if imagen_subida:
        imagen = imagen_subida

    # Video: archivo o URL (opcional).
    video = request.form.get('video', '')
    video_subido = guardar_video_noticia(request.files.get('video_file'))
    if video_subido:
        video = video_subido

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO noticias (titulo, descripcion, imagen, video, fuente, fecha, link, categoria, es_externa)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0)
    """, (titulo, descripcion, imagen, video, fuente, fecha, link, categoria))
    # Registra la categoría como área/orientación para que aparezca en los dropdowns.
    registrar_orientaciones([categoria])
    db.commit()
    flash('Noticia agregada exitosamente.', 'success')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_noticia(id):
    titulo = request.form.get('titulo', '')
    descripcion = request.form.get('descripcion', '')
    fuente = request.form.get('fuente', '')
    fecha = request.form.get('fecha', '')
    link = request.form.get('link', '')
    categoria = request.form.get('categoria', 'General')

    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Imagen: si se sube archivo nuevo se usa; si no, se usa la URL del
    # formulario; y si ambas están vacías, se conserva la imagen actual.
    imagen_subida = guardar_imagen_noticia(request.files.get('imagen_file'))
    if imagen_subida:
        imagen = imagen_subida
    else:
        imagen_form = request.form.get('imagen', '').strip()
        if imagen_form:
            imagen = imagen_form
        else:
            cursor.execute("SELECT imagen FROM noticias WHERE id = %s", (id,))
            actual = cursor.fetchone()
            imagen = actual['imagen'] if actual else ''

    # Video: archivo nuevo, o URL del formulario, o conservar el actual.
    video = request.form.get('video', '').strip()
    video_subido = guardar_video_noticia(request.files.get('video_file'))
    if video_subido:
        video = video_subido
    elif not video:
        cursor.execute("SELECT video FROM noticias WHERE id = %s", (id,))
        actual_video = cursor.fetchone()
        video = actual_video['video'] if (actual_video and actual_video['video']) else ''

    cursor.execute("""
        UPDATE noticias
        SET titulo = %s, descripcion = %s, imagen = %s, video = %s, fuente = %s, fecha = %s, link = %s, categoria = %s
        WHERE id = %s
    """, (titulo, descripcion, imagen, video, fuente, fecha, link, categoria, id))
    # Registra la categoría como área/orientación para que aparezca en los dropdowns.
    registrar_orientaciones([categoria])
    db.commit()
    flash('Noticia actualizada exitosamente.', 'success')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_noticia(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM noticias WHERE id = %s", (id,))
    db.commit()
    flash('Noticia eliminada.', 'info')
    return redirect(url_for('admin_noticias.admin_noticias'))


# --- FUENTES DE NOTICIAS ---

@bp.route('/admin/noticias/fuentes/nueva', methods=['POST'])
@requiere_admin
def nueva_fuente():
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la fuente no puede estar vacío.', 'danger')
        return redirect(url_for('admin_noticias.admin_noticias'))

    asegurar_tabla_fuentes()
    db = obtener_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO fuentes (nombre) VALUES (%s)", (nombre,))
        db.commit()
        flash(f'Fuente "{nombre}" agregada.', 'success')
    except Exception:
        db.rollback()
        flash('Esa fuente ya está registrada.', 'warning')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/fuentes/editar/<int:id>', methods=['POST'])
@requiere_admin
def editar_fuente(id):
    nombre = request.form.get('nombre', '').strip()
    if not nombre:
        flash('El nombre de la fuente no puede estar vacío.', 'danger')
        return redirect(url_for('admin_noticias.admin_noticias'))
    db = obtener_db()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE fuentes SET nombre = %s WHERE id = %s", (nombre, id))
        db.commit()
        flash('Fuente actualizada.', 'success')
    except Exception:
        db.rollback()
        flash('Ese nombre ya está en uso por otra fuente.', 'warning')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/fuentes/toggle/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def toggle_fuente(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("UPDATE fuentes SET activo = NOT activo WHERE id = %s", (id,))
    db.commit()
    flash('Visibilidad de la fuente actualizada.', 'success')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/fuentes/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_fuente(id):
    asegurar_tabla_fuentes()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT nombre FROM fuentes WHERE id = %s", (id,))
    fila = cursor.fetchone()
    if not fila:
        flash('Fuente no encontrada.', 'warning')
        return redirect(url_for('admin_noticias.admin_noticias'))
    cur = db.cursor()
    # Registra la fuente como eliminada para que no se vuelva a auto-registrar.
    cur.execute("INSERT IGNORE INTO fuentes_eliminadas (nombre) VALUES (%s)", (fila['nombre'],))
    cur.execute("DELETE FROM fuentes WHERE id = %s", (id,))
    db.commit()
    flash(f'Fuente "{fila["nombre"]}" eliminada.', 'info')
    return redirect(url_for('admin_noticias.admin_noticias'))


# --- FILTROS DE FECHA DEL BUSCADOR DE NOTICIAS ---

@bp.route('/admin/noticias/filtros-fecha/editar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def editar_filtro_fecha(id):
    # El formulario de renombrar envía "etiqueta"; el toggle de visibilidad solo envía "activo".
    if 'etiqueta' in request.form:
        etiqueta = request.form.get('etiqueta', '').strip()
        if not etiqueta:
            flash('La etiqueta del filtro no puede estar vacía.', 'danger')
            return redirect(url_for('admin_noticias.admin_noticias'))
        db = obtener_db()
        cursor = db.cursor()
        cursor.execute("UPDATE filtros_fecha SET etiqueta = %s WHERE id = %s", (etiqueta, id))
        db.commit()
        flash('Filtro de fecha actualizado.', 'success')
    else:
        activo = 1 if request.form.get('activo') else 0
        db = obtener_db()
        cursor = db.cursor()
        cursor.execute("UPDATE filtros_fecha SET activo = %s WHERE id = %s", (activo, id))
        db.commit()
        flash('Visibilidad del filtro actualizada.', 'success')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/filtros-fecha/mover/<int:id>/<direccion>', methods=['POST'])
@requiere_admin
def mover_filtro_fecha(id, direccion):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM filtros_fecha ORDER BY orden, id")
    filas = cursor.fetchall()
    idx = next((i for i, f in enumerate(filas) if f['id'] == id), None)
    if idx is None:
        return redirect(url_for('admin_noticias.admin_noticias'))
    if direccion == 'arriba' and idx > 0:
        filas[idx], filas[idx - 1] = filas[idx - 1], filas[idx]
    elif direccion == 'abajo' and idx < len(filas) - 1:
        filas[idx], filas[idx + 1] = filas[idx + 1], filas[idx]
    else:
        flash('El filtro ya está en el límite.', 'info')
        return redirect(url_for('admin_noticias.admin_noticias'))
    for orden, f in enumerate(filas):
        cursor.execute("UPDATE filtros_fecha SET orden = %s WHERE id = %s", (orden, f['id']))
    db.commit()
    flash('Orden de los filtros actualizado.', 'success')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/filtros-fecha/nueva', methods=['POST'])
@requiere_admin
def nueva_filtro_fecha():
    etiqueta = request.form.get('etiqueta', '').strip()
    desde = request.form.get('desde', '').strip()
    hasta = request.form.get('hasta', '').strip()
    activo = 1 if request.form.get('activo') else 0

    if not etiqueta:
        flash('El nombre del filtro no puede estar vacío.', 'danger')
        return redirect(url_for('admin_noticias.admin_noticias'))

    def fecha_valida(valor):
        try:
            datetime.strptime(valor, '%Y-%m-%d')
            return True
        except (ValueError, TypeError):
            return False

    if not desde:
        flash('Seleccioná la fecha desde la que se muestran las noticias.', 'danger')
        return redirect(url_for('admin_noticias.admin_noticias'))
    if not fecha_valida(desde):
        flash('La fecha "desde" no es válida.', 'danger')
        return redirect(url_for('admin_noticias.admin_noticias'))
    if hasta and not fecha_valida(hasta):
        flash('La fecha "hasta" no es válida.', 'danger')
        return redirect(url_for('admin_noticias.admin_noticias'))

    if desde and hasta:
        condicion = f"fecha >= '{desde}' AND fecha <= '{hasta}'"
    else:
        condicion = f"fecha >= '{desde}'"

    asegurar_tabla_filtros_fecha()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Generar un "valor" único (clave usada en la URL) a partir de la etiqueta.
    base = re.sub(r'[^a-z0-9]+', '_',
                  etiqueta.lower()
                  .replace('á', 'a').replace('é', 'e').replace('í', 'i')
                  .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
                  ).strip('_')
    valor = base or 'filtro'
    sufijo = 2
    cursor.execute("SELECT COUNT(*) AS n FROM filtros_fecha WHERE valor = %s", (valor,))
    while cursor.fetchone()['n'] > 0:
        valor = f"{base}_{sufijo}"
        sufijo += 1
        cursor.execute("SELECT COUNT(*) AS n FROM filtros_fecha WHERE valor = %s", (valor,))

    cursor.execute("SELECT COALESCE(MAX(orden), 0) AS m FROM filtros_fecha")
    orden = cursor.fetchone()['m'] + 1

    cur = db.cursor()
    cur.execute(
        "INSERT INTO filtros_fecha (valor, etiqueta, condicion, activo, orden, es_fijo) VALUES (%s, %s, %s, %s, %s, 0)",
        (valor, etiqueta, condicion, activo, orden)
    )
    db.commit()
    if hasta:
        flash(f'Filtro "{etiqueta}" agregado (del {desde} al {hasta}).', 'success')
    else:
        flash(f'Filtro "{etiqueta}" agregado (desde {desde}).', 'success')
    return redirect(url_for('admin_noticias.admin_noticias'))


@bp.route('/admin/noticias/filtros-fecha/eliminar/<int:id>', methods=['POST'])
@requiere_admin
@ajax_o_redirect
def eliminar_filtro_fecha(id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM filtros_fecha WHERE id = %s", (id,))
    db.commit()
    flash('Filtro eliminado.', 'info')
    return redirect(url_for('admin_noticias.admin_noticias'))
