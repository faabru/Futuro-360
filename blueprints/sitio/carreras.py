"""
Rutas del catálogo de carreras del sitio público.

- ``carreras``            → listado con filtros por área y búsqueda.
- ``detalle_carrera``     → página individual o genérica de una carrera.
- ``buscar_universidades`` → API DDG para universidades, descubrimiento y fallback.
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

    filtro = request.args.get('filtro', 'populares')  # populares | todas | [área]
    busqueda = request.args.get('q', '').strip()

    # Áreas disponibles: orientaciones del admin + áreas reales de carreras.
    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [r['nombre'] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT area_profesional FROM carreras ORDER BY area_profesional")
    areas_carreras = [r['area_profesional'] for r in cursor.fetchall()]
    areas_disponibles = list(dict.fromkeys(areas_registradas + areas_carreras))

    area_actual = 'todas'
    filtro_actual = filtro

    # Se traen todas las carreras; el filtrado por área y búsqueda se hace en JS.
    query = "SELECT * FROM carreras ORDER BY nombre ASC"
    cursor.execute(query)
    lista_carreras = cursor.fetchall()

    # Áreas de cada carrera (una carrera puede tener varias vía carrera_areas).
    cursor.execute("SELECT carrera_id, area FROM carrera_areas ORDER BY id")
    areas_por_carrera = {}
    for r in cursor.fetchall():
        areas_por_carrera.setdefault(r['carrera_id'], []).append(r['area'])
    for carrera in lista_carreras:
        areas = areas_por_carrera.get(carrera['id'], [])
        if not areas and carrera.get('area_profesional'):
            areas = [carrera['area_profesional']]
        carrera['areas'] = areas

    # --- POPULARIDAD AUTOMÁTICA (según los tests) ---
    # Cuenta cuántas veces se eligió cada área como ganadora en los tests.
    # Las áreas más elegidas determinan cuáles carreras son "populares".
    cursor.execute("""
        SELECT area_profesional_sugerida AS area, COUNT(*) AS total
        FROM resultados
        GROUP BY area_profesional_sugerida
        ORDER BY total DESC, area ASC
    """)
    conteos = cursor.fetchall()
    popularidad_area = {r['area']: r['total'] for r in conteos}

    # Áreas populares (las que tienen al menos una elección en los tests).
    # Si todavía no hay ningún resultado, se consideran todas las áreas para
    # que el filtro "Populares" (que es el predeterminado) no quede vacío.
    if conteos:
        areas_populares = [r['area'] for r in conteos]
    else:
        areas_populares = list(areas_disponibles)

    # Popularidad por carrera: suma de elecciones de sus áreas. Se usa para
    # ordenar el filtro "Populares" (más elegidas primero).
    for carrera in lista_carreras:
        areas_populares_carrera = []
        popularidad = 0
        for area in carrera['areas']:
            v = popularidad_area.get(area, 0)
            if v > 0:
                areas_populares_carrera.append(area)
                popularidad += v
        carrera['areas_populares'] = areas_populares_carrera
        carrera['popularidad'] = popularidad

    return render_template('carreras.html',
        carreras=lista_carreras,
        filtro_actual=filtro,
        area_actual=area_actual,
        busqueda=busqueda,
        areas_disponibles=areas_disponibles,
        areas_populares=areas_populares
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

    # Universidades que dictan la carrera; públicas primero, alfabético después.
    cursor.execute("""
        SELECT u.id, u.nombre, u.siglas, u.tipo, u.sitio_web
        FROM carrera_universidad cu
        JOIN universidades u ON u.id = cu.universidad_id
        WHERE cu.carrera_id = %s AND u.activo = 1
        ORDER BY FIELD(u.tipo, 'publica', 'privada'), u.nombre
    """, (carrera_id,))
    universidades = cursor.fetchall()

    # Busca template individual (ej: carreras/carrera_39.html); si no existe, usa el genérico.
    template_individual = f'carreras/carrera_{carrera_id}.html'
    template_path = os.path.join(current_app.template_folder, template_individual)

    if os.path.exists(template_path):
        return render_template(template_individual, carrera=carrera, universidades=universidades)
    else:
        return render_template('carrera_detalle.html', carrera=carrera, universidades=universidades)


@bp.route('/carrera/<int:carrera_id>/buscar-universidades')
def buscar_universidades(carrera_id):
    """API de búsqueda vía DuckDuckGo con 4 modos:
    ?universidad_id=N            → carrera en sitio oficial (valida puente).
    ?universidad_id=N&modo=info  → noticias/infos sobre la universidad.
    ?descubrir=1                 → carrera en el resto del catálogo.
    Sin params                   → búsqueda general (fallback).
    """
    if g.user is None:
        return {"error": "Sesión expirada. Por favor iniciá sesión nuevamente.", "resultados": [], "status": "unauthorized"}, 401

    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()

    if not carrera:
        return {"error": "Carrera no encontrada", "resultados": []}, 404

    def _buscar(query, max_results=5):
        """DDG search → lista de {titulo, url, descripcion}."""
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
        # --- Descubrimiento: busca la carrera en universidades no relacionadas ---
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
                    continue
                # Filtra resultados que realmente están dentro del dominio.
                res = [r for r in res if u["sitio_web"] in (r["url"] or "")]
                if res:
                    encontradas.append({
                        "id": u["id"], "nombre": u["nombre"], "siglas": u["siglas"],
                        "tipo": u["tipo"], "sitio_web": u["sitio_web"],
                        "resultados": res,
                    })
            return {"encontradas": encontradas, "status": "success"}, 200

        # --- Enlaces por universidad: carrera o info/noticias ---
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
            resultados = _buscar(query_base, max_results=5)
        else:
            # Búsqueda general: usa las universidades VERIFICADAS que dictan la
            # carrera en Tucumán (tabla carrera_universidad) y trae los links de
            # sus sitios oficiales. Así solo aparecen universidades donde sí se
            # dicta la carrera. Si no hay relaciones cargadas, cae a DDG genérico.
            cursor.execute("""
                SELECT u.id, u.nombre, u.siglas, u.tipo, u.sitio_web
                FROM carrera_universidad cu
                JOIN universidades u ON u.id = cu.universidad_id
                WHERE cu.carrera_id = %s AND u.activo = 1
                ORDER BY FIELD(u.tipo, 'publica', 'privada'), u.nombre
            """, (carrera_id,))
            verificadas = cursor.fetchall()

            resultados = []
            if verificadas:
                for u in verificadas:
                    try:
                        res = _buscar(
                            f'site:{u["sitio_web"]} "{carrera["nombre"]}"',
                            max_results=3)
                    except Exception:
                        res = []
                    # Solo enlaces dentro del dominio oficial de la universidad.
                    res = [r for r in res if u["sitio_web"] in (r["url"] or "")]
                    if not res:
                        # Fallback: link directo al sitio oficial (sabemos que la dicta).
                        res = [{
                            "titulo": f'Carrera de {carrera["nombre"]} - {u["nombre"]}',
                            "url": f'https://{u["sitio_web"]}',
                            "descripcion": (
                                f'Sitio oficial de {u["nombre"]} '
                                f'(Universidad {"Pública" if u["tipo"] == "publica" else "Privada"})'
                            ),
                        }]
                    for r in res[:3]:
                        r.setdefault("titulo", u["nombre"])
                        resultados.append(r)
            else:
                # Sin relaciones cargadas: búsqueda genérica en DDG acotada a Tucumán.
                query_base = f'"{carrera["nombre"]}" carrera universidad Tucumán'
                resultados = _buscar(query_base, max_results=8)

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
