"""
Dashboard del panel de administración.

Pantalla principal con tablas resumen y estadísticas para gráficos (mejora TFI:
visualización de información con Chart.js).
"""

from datetime import datetime

from flask import (Blueprint, jsonify, render_template, request)

from config import Config
from core.decoradores import es_usuario_dueño, requiere_admin
from core.migraciones import asegurar_tabla_orientaciones
from database_handler import obtener_db

bp = Blueprint('admin', __name__)


@bp.route('/admin')
@requiere_admin
def admin_dashboard():
    asegurar_tabla_orientaciones()
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    total_usuarios = cursor.fetchone()['total']

    f_nombre = request.args.get('nombre', '').strip()
    f_email = request.args.get('email', '').strip()
    f_fecha = request.args.get('fecha', '').strip()

    where = []
    params = []
    if f_nombre:
        where.append("(nombre LIKE %s OR apellido LIKE %s)")
        params.extend(['%' + f_nombre + '%'] * 2)
    if f_email:
        where.append("email LIKE %s")
        params.append('%' + f_email + '%')
    if f_fecha:
        where.append("DATE(created_at) = %s")
        params.append(f_fecha)

    sql = "SELECT id, nombre, apellido, email, rol, activo, created_at FROM usuarios"
    if where:
        sql += " WHERE " + " AND ".join(where)
    cursor.execute(sql, params)
    usuarios = cursor.fetchall()

    # Fragmento AJAX: solo la tabla de usuarios (para recargar sin refrescar).
    if request.args.get('fragmento') == '1':
        return render_template('admin/_tabla_usuarios.html', usuarios=usuarios,
                               email_dueño=Config.ADMIN_EMAIL,
                               es_dueño=es_usuario_dueño())

    cursor.execute("SELECT * FROM carreras")
    carreras = cursor.fetchall()

    cursor.execute("SELECT * FROM preguntas")
    preguntas = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM noticias")
    total_noticias = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM noticias WHERE fecha = CURDATE()")
    noticias_hoy = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM game_carreras WHERE activo = 1")
    carreras_juego_activas = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM game_preguntas WHERE activo = 1")
    preguntas_juego_activas = cursor.fetchone()['total']

    cursor.execute("SELECT * FROM orientaciones ORDER BY nombre")
    orientaciones = cursor.fetchall()

    # --- ESTADÍSTICAS PARA GRÁFICOS (mejora TFI: visualización de información) ---
    # Usuarios conectados en los últimos 5 minutos (presencia "en línea").
    try:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM sesiones_activas "
            "WHERE last_seen >= NOW() - INTERVAL 5 MINUTE")
        usuarios_activos = cursor.fetchone()['total']
    except Exception:
        usuarios_activos = 0

    cursor.execute("SELECT COUNT(*) AS total FROM tests")
    total_tests = cursor.fetchone()['total']

    # Usuarios distintos que realizaron al menos un test (para mostrar
    # "N tests realizados por M estudiantes").
    cursor.execute(
        "SELECT COUNT(DISTINCT usuario_id) AS total FROM tests")
    usuarios_con_tests = cursor.fetchone()['total']

    # Tests por mes (últimos 6 meses, completando los meses sin actividad).
    cursor.execute(
        """SELECT DATE_FORMAT(fecha_realizacion, '%Y-%m') AS mes, COUNT(*) AS total
           FROM tests
           WHERE fecha_realizacion >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
           GROUP BY mes ORDER BY mes""")
    tests_por_mes = cursor.fetchall()
    meses_map = {r['mes']: r['total'] for r in tests_por_mes}
    _meses_nombre = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                     'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    series_tests = []
    now = datetime.now()
    for i in range(5, -1, -1):
        # Retroceder i meses desde el mes actual sin librerías externas.
        anio, mes = now.year, now.month
        for _ in range(i):
            mes -= 1
            if mes == 0:
                mes = 12
                anio -= 1
        clave = f"{anio:04d}-{mes:02d}"
        series_tests.append({
            'mes': _meses_nombre[mes - 1],
            'total': meses_map.get(clave, 0)
        })

    # Usuarios por área profesional sugerida.
    cursor.execute(
        """SELECT COALESCE(a.nombre, r.area_profesional_sugerida, 'Sin área') AS area, COUNT(*) AS total
           FROM resultados r
           LEFT JOIN areas a ON r.area_id = a.id
           GROUP BY area ORDER BY total DESC LIMIT 8""")
    usuarios_por_area = cursor.fetchall()

    # Noticias por fuente y por categoría.
    cursor.execute(
        """SELECT fuente, COUNT(*) AS total FROM noticias
           GROUP BY fuente ORDER BY total DESC LIMIT 8""")
    noticias_por_fuente = cursor.fetchall()

    cursor.execute(
        """SELECT categoria, COUNT(*) AS total FROM noticias
           GROUP BY categoria ORDER BY total DESC LIMIT 8""")
    noticias_por_categoria = cursor.fetchall()

    return render_template('admin/dashboard.html',
        usuarios=usuarios, total_usuarios=total_usuarios,
        f_nombre=f_nombre, f_email=f_email, f_fecha=f_fecha,
        carreras=carreras, preguntas=preguntas,
        total_noticias=total_noticias, noticias_hoy=noticias_hoy,
        carreras_juego_activas=carreras_juego_activas,
        preguntas_juego_activas=preguntas_juego_activas,
        orientaciones=orientaciones, email_dueño=Config.ADMIN_EMAIL,
        es_dueño=es_usuario_dueño(),
        usuarios_activos=usuarios_activos, total_tests=total_tests,
        usuarios_con_tests=usuarios_con_tests,
        tests_por_mes=series_tests, usuarios_por_area=usuarios_por_area,
        noticias_por_fuente=noticias_por_fuente,
        noticias_por_categoria=noticias_por_categoria)


@bp.route('/admin/usuarios-en-linea')
@requiere_admin
def admin_usuarios_en_linea():
    """Devuelve (JSON) la cantidad de usuarios conectados en los últimos 5 min,
    para que el dashboard la refresque en tiempo real sin recargar la página."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM sesiones_activas "
            "WHERE last_seen >= NOW() - INTERVAL 5 MINUTE")
        total = cursor.fetchone()['total']
    except Exception:
        total = 0
    return jsonify(total=total)
