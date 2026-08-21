"""
Rutas del catálogo de carreras del sitio público.

- ``carreras``           → listado con filtros por área y búsqueda.
- ``detalle_carrera``    → página de una carrera (usa template individual si existe).
- ``buscar_universidades``→ búsqueda web de universidades (API de DuckDuckGo).
"""

import os

from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, url_for)

from core.decoradores import requiere_login
from core.migraciones import asegurar_tabla_orientaciones, obtener_areas_carrera
from database_handler import obtener_db

bp = Blueprint('carreras', __name__)


@bp.route('/carreras')
@requiere_login
def carreras():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    filtro = request.args.get('filtro', 'populares')  # populares | todas | [área profesional]
    busqueda = request.args.get('q', '').strip()

    # Determinar si el filtro es un área profesional, populares o todas.
    # Las áreas disponibles vienen de la tabla de orientaciones (gestionada desde
    # el panel admin) + las áreas ya asignadas a carreras en la base.
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT area_profesional FROM carreras ORDER BY area_profesional")
    areas_carreras = [r['area_profesional'] for r in cursor.fetchall()]
    areas_disponibles = list(dict.fromkeys(areas_registradas + areas_carreras))

    area_actual = 'todas'
    filtro_actual = filtro
    es_populares = filtro == 'populares'

    # Traemos todas las carreras: el filtrado por área y la búsqueda se realizan
    # en el cliente (JS) para no recargar la página al buscar o filtrar.
    query = "SELECT * FROM carreras ORDER BY popular DESC, nombre ASC"
    cursor.execute(query)
    lista_carreras = cursor.fetchall()

    # Adjuntar todas las áreas de cada carrera (una carrera puede tener varias).
    cursor.execute("SELECT carrera_id, area FROM carrera_areas ORDER BY id")
    areas_por_carrera = {}
    for r in cursor.fetchall():
        areas_por_carrera.setdefault(r['carrera_id'], []).append(r['area'])
    for carrera in lista_carreras:
        areas = areas_por_carrera.get(carrera['id'], [])
        if not areas and carrera.get('area_profesional'):
            areas = [carrera['area_profesional']]
        carrera['areas'] = areas

    return render_template('carreras.html',
        carreras=lista_carreras,
        filtro_actual=filtro,
        area_actual=area_actual,
        busqueda=busqueda,
        areas_disponibles=areas_disponibles
    )


@bp.route('/carrera/<int:carrera_id>')
@requiere_login
def detalle_carrera(carrera_id):
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()
    if not carrera:
        flash('No pudimos encontrar información sobre esa carrera.', 'danger')
        return redirect(url_for('carreras.carreras'))

    areas = obtener_areas_carrera(carrera_id)
    if not areas and carrera.get('area_profesional'):
        areas = [carrera['area_profesional']]
    carrera['areas'] = areas

    # Universidades de Tucumán que dictan esta carrera (tabla puente).
    # Públicas primero, luego privadas, alfabético dentro de cada grupo.
    cursor.execute("""
        SELECT u.id, u.nombre, u.siglas, u.tipo, u.sitio_web
        FROM carrera_universidad cu
        JOIN universidades u ON u.id = cu.universidad_id
        WHERE cu.carrera_id = %s AND u.activo = 1
        ORDER BY FIELD(u.tipo, 'publica', 'privada'), u.nombre
    """, (carrera_id,))
    universidades = cursor.fetchall()

    # Verificar si existe un template HTML individual para esta carrera.
    # Ejemplo: templates/carreras/carrera_39.html para Arquitectura (id=39).
    template_individual = f'carreras/carrera_{carrera_id}.html'
    template_path = os.path.join(current_app.template_folder, template_individual)

    if os.path.exists(template_path):
        # Usar el template personalizado de esta carrera específica.
        return render_template(template_individual, carrera=carrera, universidades=universidades)
    else:
        # Fallback al template genérico — ninguna carrera queda sin página.
        return render_template('carrera_detalle.html', carrera=carrera, universidades=universidades)


@bp.route('/carrera/<int:carrera_id>/buscar-universidades')
def buscar_universidades(carrera_id):
    """Busca enlaces sobre esta carrera (API de DuckDuckGo).

    Modos (mutuamente excluyentes):
    - ``?universidad_id=N``: enlaces de esta carrera en el sitio oficial de
      esa universidad (valida que esté relacionada en la puente).
    - ``?universidad_id=N&modo=info``: enlaces informativos y noticias sobre
      esa universidad, sin restringir el dominio.
    - ``?descubrir=1``: busca esta carrera en el resto del catálogo de
      universidades; solo devuelve las que tienen al menos un resultado real
      dentro de su dominio.
    - Sin parámetros: búsqueda general (fallback para carreras sin datos).
    """
    # Verificar sesión manualmente para poder responder JSON si no está logueado.
    if g.user is None:
        return {"error": "Sesión expirada. Por favor iniciá sesión nuevamente.", "resultados": [], "status": "unauthorized"}, 401

    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()

    if not carrera:
        return {"error": "Carrera no encontrada", "resultados": []}, 404

    def _buscar(query, max_results=5):
        """Ejecuta la búsqueda y devuelve resultados ya con dominio verificado."""
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "titulo": item.get("title", ""),
                "url": item.get("href", "#"),
                "descripcion": item.get("body", "")
            }
            for item in results
        ]

    universidad_id = request.args.get('universidad_id', type=int)
    modo = request.args.get('modo', 'carrera')

    try:
        # --- Descubrimiento: otras universidades del catálogo que la dictan ---
        if request.args.get('descubrir'):
            cursor.execute("""
                SELECT u.id, u.nombre, u.siglas, u.tipo, u.sitio_web
                FROM universidades u
                WHERE u.activo = 1 AND u.id NOT IN (
                    SELECT universidad_id FROM carrera_universidad WHERE carrera_id = %s
                )
                ORDER BY u.nombre
            """, (carrera_id,))
            candidatas = cursor.fetchall()

            encontradas = []
            for u in candidatas:
                try:
                    res = _buscar(f'site:{u["sitio_web"]} "{carrera["nombre"]}"', max_results=3)
                except Exception:
                    continue  # una universidad que falla no tira las demás
                # Solo resultados realmente dentro del dominio (descarta publicidad).
                res = [r for r in res if u["sitio_web"] in (r["url"] or "")]
                if res:
                    encontradas.append({
                        "id": u["id"], "nombre": u["nombre"], "siglas": u["siglas"],
                        "tipo": u["tipo"], "sitio_web": u["sitio_web"],
                        "resultados": res,
                    })
            return {"encontradas": encontradas, "status": "success"}, 200

        # --- Enlaces por universidad (carrera o info/noticias) ---
        universidad = None
        if universidad_id:
            cursor.execute("""
                SELECT u.id, u.nombre, u.sitio_web
                FROM carrera_universidad cu
                JOIN universidades u ON u.id = cu.universidad_id
                WHERE cu.carrera_id = %s AND u.id = %s AND u.activo = 1
            """, (carrera_id, universidad_id))
            universidad = cursor.fetchone()
            if not universidad:
                return {"error": "Esa universidad no está asociada a la carrera", "resultados": []}, 400

            if modo == 'info':
                query_base = f'universidad {universidad["nombre"]} noticias'
            else:
                query_base = f'site:{universidad["sitio_web"]} "{carrera["nombre"]}"'
        else:
            # Búsqueda general enfocada en la carrera y la ubicación.
            query_base = f"{carrera['nombre']} universidad facultad Tucumán site:edu.ar OR site:gov.ar"

        if not query_base:
            return {"error": "Consulta vacía", "resultados": []}, 400

        resultados = _buscar(query_base)

        return {
            "resultados": resultados,
            "total": len(resultados),
            "universidad": universidad["nombre"] if universidad else None,
            "status": "success"
        }, 200

    except Exception as e:
        return {
            "error": f"Error interno del servidor al buscar en DDG: {str(e)}",
            "resultados": [],
            "status": "server_error"
        }, 500
