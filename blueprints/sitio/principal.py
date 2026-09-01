"""
Rutas principales del sitio público: portada, dashboard del usuario y el
formulario de comentarios del pie de página.

- ``index``     → portada (si ya hay sesión, redirige al dashboard).
- ``dashboard`` → home privado con el resumen de la actividad del usuario.
- ``enviar_comentario`` → guarda un mensaje del pie de página (tabla comentarios).
"""

import json

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)

from core.decoradores import requiere_login
from database_handler import obtener_db

bp = Blueprint('principal', __name__)


@bp.route('/')
def index():
    """Portada pública de Futuro 360."""
    if g.user:
        return redirect(url_for('principal.dashboard'))
    return render_template('index.html')


@bp.route('/dashboard')
@requiere_login
def dashboard():
    """Home privado del usuario: historial, estadísticas y novedades."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Últimos 3 tests realizados, con el texto legible del detalle.
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion,
               r.detalle
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
        LIMIT 3
    """, (g.user['id'],))
    historial_raw = cursor.fetchall()

    historial = []
    for item in historial_raw:
        detalle_corto = ''
        try:
            detalle_data = json.loads(item['detalle'])
            resumen = detalle_data.get('resumen') or []
            texto = detalle_data.get('texto') or ''
        except Exception:
            resumen = []
            texto = item['detalle'] or ''

        if resumen:
            # Texto corto para el historial: solo las 2-3 áreas principales.
            top = resumen[:3]
            detalle_corto = ' · '.join(
                f"{r.get('area', '').strip()}: {r.get('puntos', 0)}" for r in top
            ).strip()
        if not detalle_corto:
            detalle_corto = (texto or '').strip() or (item['detalle'] or '')
        # Límite de seguridad: nunca más de 90 caracteres para no desbordar el bloque.
        if len(detalle_corto) > 90:
            detalle_corto = detalle_corto[:90].rsplit(' ', 1)[0] + '…'
        item['detalle_texto'] = detalle_corto
        historial.append(item)

    # Total de tests realizados por el usuario.
    cursor.execute("""
        SELECT COUNT(*) AS total, MAX(t.fecha_realizacion) AS ultima_fecha
        FROM tests t
        WHERE t.usuario_id = %s
    """, (g.user['id'],))
    stats_tests = cursor.fetchone()
    total_tests = stats_tests['total'] if stats_tests else 0
    ultima_fecha_test = stats_tests['ultima_fecha'] if stats_tests else None

    # Total de carreras y de noticias recientes para la sección de novedades.
    cursor.execute("SELECT COUNT(*) AS total FROM carreras")
    total_carreras = cursor.fetchone()['total']

    cursor.execute("""
        SELECT id, titulo, fuente, fecha
        FROM noticias
        WHERE fecha IS NOT NULL
        ORDER BY fecha DESC
        LIMIT 3
    """)
    noticias_recientes = cursor.fetchall()

    return render_template('dashboard.html',
        historial=historial,
        total_tests=total_tests,
        ultima_fecha_test=ultima_fecha_test,
        total_carreras=total_carreras,
        noticias_recientes=noticias_recientes)


@bp.route('/comentar', methods=['POST'])
def enviar_comentario():
    """Guarda un mensaje enviado desde el formulario del pie de página."""
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    if not mensaje:
        flash('Por favor, escribe un mensaje antes de enviar.', 'danger')
        return redirect(request.referrer or url_for('principal.index'))

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO comentarios (nombre, email, mensaje) VALUES (%s, %s, %s)",
        (nombre, email, mensaje))
    db.commit()
    flash('¡Muchas gracias por tu mensaje! Lo hemos recibido correctamente.', 'success')
    return redirect(request.referrer or url_for('principal.index'))
