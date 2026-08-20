"""
Rutas de la sección de noticias del sitio público.

- ``noticias`` → listado con filtros de fecha, fuente y categoría (búsqueda
                 en el cliente por JS).
"""

from flask import Blueprint, render_template, request

from core.decoradores import requiere_login
from core.migraciones import (asegurar_tabla_filtros_fecha, asegurar_tabla_fuentes,
                              asegurar_tabla_orientaciones, condicion_fecha_segura)
from database_handler import obtener_db

bp = Blueprint('noticias', __name__)


@bp.route('/noticias')
@requiere_login
def noticias():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Filtros recibidos por query string.
    filtro_fecha = request.args.get('fecha', 'todas')
    filtro_fuente = request.args.get('fuente', 'todas')
    filtro_categoria = request.args.get('categoria', 'todas')
    busqueda = request.args.get('q', '').strip()

    asegurar_tabla_filtros_fecha()

    # Construir query dinámica con filtros.
    query = "SELECT * FROM noticias WHERE 1=1"
    params = []

    # Filtro por fecha: usa la condición guardada en la tabla filtros_fecha.
    # Se valida con la whitelist estricta condicion_fecha_segura (la misma que
    # usa el panel admin), que permite tanto los presets fijos como los rangos
    # personalizados que el admin crea desde el panel. Así un filtro
    # personalizado funciona igual en la página pública y en el panel.
    if filtro_fecha != 'todas':
        cursor.execute("SELECT condicion FROM filtros_fecha WHERE valor = %s", (filtro_fecha,))
        fila_fecha = cursor.fetchone()
        condicion = fila_fecha['condicion'] if fila_fecha else ''
        if condicion_fecha_segura(condicion):
            query += " AND " + condicion

    if filtro_fuente != 'todas':
        query += " AND fuente = %s"
        params.append(filtro_fuente)

    # La búsqueda por texto y la categoría se filtran en el cliente (JS) para
    # no recargar la página. La fecha y la fuente se mantienen del lado servidor.
    query += " ORDER BY fecha DESC, id DESC"

    cursor.execute(query, params)
    items_noticias = cursor.fetchall()

    # Obtener fuentes y categorías únicas para los filtros.
    # Las fuentes visibles son las registradas (activas) en la tabla fuentes,
    # más las fuentes de noticias que todavía no están registradas en la tabla.
    asegurar_tabla_fuentes()
    cursor.execute("SELECT nombre FROM fuentes WHERE activo = 1 ORDER BY nombre")
    fuentes_activas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes")
    todas_registradas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT nombre FROM fuentes_eliminadas")
    fuentes_eliminadas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT fuente FROM noticias ORDER BY fuente")
    fuentes_noticias = [row['fuente'] for row in cursor.fetchall()]
    fuentes = list(dict.fromkeys(
        fuentes_activas + [f for f in fuentes_noticias if f not in todas_registradas and f not in fuentes_eliminadas]
    ))

    asegurar_tabla_orientaciones()
    cursor.execute("SELECT nombre FROM orientaciones ORDER BY nombre")
    areas_registradas = [row['nombre'] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT categoria FROM noticias ORDER BY categoria")
    categorias_noticias = [row['categoria'] for row in cursor.fetchall()]
    categorias = list(dict.fromkeys(areas_registradas + categorias_noticias))

    asegurar_tabla_filtros_fecha()
    cursor.execute("SELECT valor, etiqueta FROM filtros_fecha WHERE activo = 1 ORDER BY orden, id")
    filtros_fecha = cursor.fetchall()

    return render_template('noticias.html',
        noticias=items_noticias,
        fuentes=fuentes,
        categorias=categorias,
        filtros_fecha=filtros_fecha,
        filtro_fecha=filtro_fecha,
        filtro_fuente=filtro_fuente,
        filtro_categoria=filtro_categoria,
        busqueda=busqueda
    )
