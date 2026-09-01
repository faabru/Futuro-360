"""
Test vocacional y resultados: test, ver resultado, PDF, historial, notas.
"""

import io
import json
import re
import traceback
from datetime import datetime

from flask import (Blueprint, Response, current_app, flash, g, redirect,
                   render_template, request, send_file, session, url_for)

from core.decoradores import requiere_login
from database_handler import obtener_db

bp = Blueprint('vocacional', __name__)

# Nombres de meses en español para fechas del informe PDF.
MESES_ES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
            'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


@bp.route('/test', methods=['GET', 'POST'])
@requiere_login
def test():
    # La pantalla de introducción siempre aparece antes de empezar: el flag se
    # consume al entrar a las preguntas, así cualquier visita a /test (navbar,
    # footer, dashboard) vuelve a pasar primero por la introducción.
    if request.method == 'GET' and not session.pop('test_iniciado', None):
        return redirect(url_for('vocacional.test_iniciar'))

    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        puntuacion = {}
        for key in request.form.keys():
            if key.startswith('q_') or key.isdigit():
                areas = request.form.getlist(key)
                for area in areas:
                    area_limpia = area.strip() if area else ''
                    # Ignorar valores nulos, vacíos o 'Neutral'.
                    if area_limpia and area_limpia != 'Neutral' and area_limpia.lower() not in ('ninguna de las anteriores', 'valor nulo'):
                        puntuacion[area_limpia] = puntuacion.get(area_limpia, 0) + 1

        # Validar que el usuario respondió algo.
        if not puntuacion:
            flash('Por favor, respondé al menos una pregunta antes de finalizar.', 'warning')
            return redirect(url_for('vocacional.test'))

        # Calcular área ganadora.
        area_ganadora = max(puntuacion, key=puntuacion.get)
        puntaje_ganador = puntuacion[area_ganadora]

        # Guardar respuestas individuales para mostrarlas después.
        respuestas_detalle = []
        for key, val in request.form.items():
            if key.startswith('opcion_'):
                pregunta_id = key.replace('opcion_', '')
                pregunta_texto = request.form.get('pregunta_' + pregunta_id, '')
                area_sel = request.form.get(pregunta_id, '')
                if area_sel == 'Neutral' or area_sel.lower() == 'valor nulo':
                    area_sel = None
                respuestas_detalle.append({
                    "pregunta": pregunta_texto,
                    "opcion": val,
                    "area": area_sel
                })

        # Construir detalle como JSON (columna tiene CHECK(json_valid)).
        resumen = [
            {"area": a, "puntos": p}
            for a, p in sorted(puntuacion.items(), key=lambda x: x[1], reverse=True)
        ]
        resumen_texto = ', '.join([f"{r['area']}: {r['puntos']} pts" for r in resumen])
        detalle_resultado_texto = (
            f"Tu área de mayor afinidad es {area_ganadora} con {puntaje_ganador} respuestas. "
            f"Desglose: {resumen_texto}."
        )
        detalle_resultado_json = json.dumps({
            "texto": detalle_resultado_texto,
            "resumen": resumen,
            "respuestas": respuestas_detalle
        }, ensure_ascii=False)

        # Mapeo de área ganadora a area_id (FK requerida por la BD).
        area_ganadora_key = area_ganadora.lower().strip()
        area_id = 1  # Fallback seguro
        if 'tecnolog' in area_ganadora_key or 'ingenier' in area_ganadora_key:
            area_id = 1
        elif 'salud' in area_ganadora_key:
            area_id = 2
        elif 'derecho' in area_ganadora_key or 'social' in area_ganadora_key:
            area_id = 3
        elif 'arte' in area_ganadora_key or 'dise' in area_ganadora_key:
            area_id = 4
        elif 'humanidades' in area_ganadora_key or 'comunicaci' in area_ganadora_key:
            area_id = 5
        elif 'naturales' in area_ganadora_key or 'agronom' in area_ganadora_key:
            area_id = 6
        elif 'negocios' in area_ganadora_key or 'econom' in area_ganadora_key:
            area_id = 7

        try:
            # Insertar el test.
            cursor.execute(
                "INSERT INTO tests (usuario_id, completado) VALUES (%s, %s)",
                (g.user['id'], 1)
            )
            id_test = cursor.lastrowid

            # Intento A: con todos los campos.
            resultado_id = None
            try:
                cursor.execute(
                    """INSERT INTO resultados
                       (test_id, area_profesional_sugerida, area_id, puntaje, detalle)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (id_test, area_ganadora, area_id, puntaje_ganador, detalle_resultado_json)
                )
                resultado_id = cursor.lastrowid
            except Exception as e1:
                # Intento B: sin puntaje como fallback.
                cursor.execute(
                    """INSERT INTO resultados
                       (test_id, area_profesional_sugerida, area_id, detalle)
                       VALUES (%s, %s, %s, %s)""",
                    (id_test, area_ganadora, area_id, detalle_resultado_json)
                )
                resultado_id = cursor.lastrowid

            db.commit()
            # Se completa el test: la próxima vez se mostrará de nuevo la
            # pantalla de información antes de comenzar.
            session.pop('test_iniciado', None)
            flash(f'¡Test completado! Tu área principal es: {area_ganadora}.', 'success')
            return redirect(url_for('vocacional.ver_resultado', resultado_id=resultado_id))

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            # No se expone el error interno al usuario (solo se registra en log).
            current_app.logger.error('Error al guardar resultado del test: %s', e)
            flash('No se pudo guardar tu resultado. Intentá de nuevo.', 'danger')
            return redirect(url_for('vocacional.test'))

    # GET: cargar preguntas con sus opciones.
    cursor.execute("SELECT * FROM preguntas ORDER BY id")
    preguntas_raw = cursor.fetchall()

    preguntas_con_opciones = []
    for p in preguntas_raw:
        cursor.execute(
            "SELECT texto_opcion, area_profesional FROM opciones_pregunta WHERE pregunta_id = %s",
            (p['id'],)
        )
        opciones = cursor.fetchall()
        preguntas_con_opciones.append({
            'id': p['id'],
            'texto_pregunta': p['texto_pregunta'],
            'opciones': [{'texto': o['texto_opcion'], 'area': o['area_profesional']} for o in opciones]
        })

    preguntas_json = json.dumps(preguntas_con_opciones, ensure_ascii=False)
    return render_template('test.html', preguntas=preguntas_raw, preguntas_json=preguntas_json)


@bp.route('/test/iniciar', methods=['GET', 'POST'])
@requiere_login
def test_iniciar():
    """Pantalla previa con la información de cómo funciona el test.

    GET muestra la información y el botón para comenzar. El POST del botón
    marca la sesión como iniciada y redirige al test real.
    """
    if request.method == 'POST':
        session['test_iniciado'] = True
        return redirect(url_for('vocacional.test'))

    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM preguntas")
    total_preguntas = cursor.fetchone()['total']
    return render_template('test_inicio.html', total_preguntas=total_preguntas)


@bp.route('/resultado/<int:resultado_id>')
@requiere_login
def ver_resultado(resultado_id):
    """Muestra el detalle de un resultado, verificando que es del usuario."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, t.fecha_realizacion
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE r.id = %s AND t.usuario_id = %s
    """, (resultado_id, g.user['id']))
    resultado = cursor.fetchone()

    if not resultado:
        flash('No se pudo encontrar el resultado solicitado.', 'danger')
        return redirect(url_for('vocacional.mis_resultados'))

    # Procesar el detalle JSON para mostrarlo como texto legible.
    resumen_puntuacion = []
    respuestas_usuario = []
    try:
        detalle_data = json.loads(resultado['detalle'])
        resultado['detalle_texto'] = detalle_data.get('texto', resultado['detalle'])
        resumen_puntuacion = detalle_data.get('resumen', [])
        respuestas_usuario = detalle_data.get('respuestas', [])
    except Exception:
        resultado['detalle_texto'] = resultado['detalle']

    # Si no hay respuestas guardadas (tests viejos), reconstruir desde el texto.
    if not respuestas_usuario and not resumen_puntuacion:
        texto = resultado['detalle_texto']
        partes = re.findall(r'([\w\s]+?):\s*(\d+)\s*pts', texto)
        resumen_puntuacion = [{"area": a.strip(), "puntos": int(p)} for a, p in partes]

    # Buscar carreras sugeridas — búsqueda flexible en 3 niveles.
    area = resultado['area_profesional_sugerida']

    cursor.execute(
        """SELECT c.* FROM carreras c
           LEFT JOIN carrera_areas ca ON ca.carrera_id = c.id
           WHERE c.area_profesional = %s OR ca.area = %s
           GROUP BY c.id LIMIT 6""",
        (area, area)
    )
    carreras_sugeridas = cursor.fetchall()

    if not carreras_sugeridas:
        cursor.execute(
            "SELECT * FROM carreras WHERE area_profesional LIKE %s LIMIT 6",
            (f"%{area}%",)
        )
        carreras_sugeridas = cursor.fetchall()

    if not carreras_sugeridas:
        cursor.execute("SELECT * FROM carreras LIMIT 6")
        carreras_sugeridas = cursor.fetchall()

    return render_template('resultado_detalle.html',
        resultado=resultado,
        carreras=carreras_sugeridas,
        resumen_puntuacion=resumen_puntuacion,
        respuestas_usuario=respuestas_usuario)


# --- INFORME PDF DEL RESULTADO VOCACIONAL (generado con WeasyPrint) ---

# Descripciones y colores por área para el comprobante PDF.
DESCRIPCIONES_AREA = {
    'Arte y Diseño': 'Tu perfil muestra una fuerte afinidad por la creatividad, '
                     'el diseño y la expresión visual. Este campo valora la '
                     'originalidad, la sensibilidad estética y la capacidad de '
                     'materializar ideas en propuestas concretas.',
    'Tecnología e Ingeniería': 'Tu perfil apunta a la resolución de problemas, la '
                               'lógica y el mundo digital. Valorás la innovación, '
                               'el razonamiento técnico y construir soluciones '
                               'que impactan en la vida cotidiana.',
    'Salud': 'Tu perfil destaca el cuidado de las personas, la empatía y el '
             'interés por el bienestar. Este campo recompensa la responsabilidad, '
             'la vocación de servicio y el trabajo metódico.',
    'Derecho y Ciencias Sociales': 'Tu perfil muestra sensibilidad por la '
                                   'sociedad, las normas y el vínculo entre las '
                                   'personas. Valorás la justicia, el análisis '
                                   'crítico y la comunicación clara.',
    'Humanidades y Comunicación': 'Tu perfil valora la palabra, el conocimiento y '
                                  'la comunicación. Este campo recompensa la '
                                  'curiosidad, la expresión y la reflexión.',
    'Ciencias Naturales y Agronomía': 'Tu perfil apunta al estudio del entorno, '
                                      'la vida y los procesos naturales. Valorás '
                                      'la investigación y el trabajo de campo.',
    'Negocios y Economía': 'Tu perfil se orienta a la gestión, el dinero y la '
                           'estrategia. Valorás la iniciativa, la organización y '
                           'la toma de decisiones.',
}


def _area_slug(area):
    """Devuelve el slug usado por los colores del anexo y del mapa."""
    a = (area or '').lower()
    if 'arte' in a or 'dise' in a:
        return 'arte'
    if 'humanidades' in a or 'comunicaci' in a:
        return 'comunicacion'
    if 'naturales' in a or 'agronom' in a:
        return 'agronomia'
    if 'salud' in a:
        return 'salud'
    if 'negocios' in a or 'econom' in a:
        return 'negocios'
    if 'derecho' in a or 'social' in a:
        return 'derecho'
    if 'tecnolog' in a or 'ingenier' in a:
        return 'tecnologia'
    return 'ciencias'


def _area_color(area):
    """Colores por área para el mapa de intereses."""
    slug = _area_slug(area)
    colores = {
        'arte':        '#22b8d8',
        'comunicacion': '#7c5cf0',
        'agronomia':   '#4a8a3e',
        'salud':       '#c98a1f',
        'negocios':    '#c25b3f',
        'derecho':     '#5c6b7d',
        'tecnologia':  '#2f52ad',
        'ciencias':    '#17a673',
    }
    return colores.get(slug, '#b9c2cf')


def _construir_contexto(resultado, usuario, carreras=None):
    """Construye el contexto de datos para el template del comprobante PDF."""
    # ── Parsear el detalle JSON: puntajes, respuestas y texto ──
    puntajes = {}
    respuestas_detalle = []
    try:
        detalle_data = json.loads(resultado.get('detalle') or '{}')
    except Exception:
        detalle_data = {}

    resumen = detalle_data.get('resumen') or []
    if resumen:
        puntajes = {r['area']: int(r['puntos']) for r in resumen if r.get('area')}
    else:
        detalle_texto = detalle_data.get('texto') or resultado.get('detalle') or ''
        matches = re.findall(r'([^:,]+):\s*(\d+)\s*pts', detalle_texto)
        puntajes = {m[0].strip(): int(m[1]) for m in matches}

    respuestas_detalle = detalle_data.get('respuestas') or []
    total_preguntas = len(respuestas_detalle)

    area_principal = resultado.get('area_profesional_sugerida', 'Sin determinar')
    notas = resultado.get('notas_personales', '').strip()
    fecha_test = resultado.get('fecha_realizacion', datetime.now())
    if hasattr(fecha_test, 'strftime'):
        fecha_str = f"{fecha_test.day} de {MESES_ES[fecha_test.month - 1]} de {fecha_test.year}"
    else:
        fecha_str = str(fecha_test)

    # ── Área líder y descripción ──
    descripcion = DESCRIPCIONES_AREA.get(
        area_principal,
        'Tu perfil refleja tus intereses vocacionales. Este es el campo donde '
        'más afinidad mostraste según tus respuestas.'
    )

    # ── Empate del primer puesto ──
    ordenado = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    top_areas = []
    empate = False
    if len(ordenado) >= 2 and ordenado[0][1] == ordenado[1][1] and ordenado[0][1] > 0:
        empate = True
        valor_max = ordenado[0][1]
        for area, pts in ordenado[:2]:
            top_areas.append({'nombre': area, 'puntaje': pts, 'max': valor_max})
    nota_empate = (
        'Detectamos un empate entre dos áreas. Esto significa que tenés intereses '
        'repartidos y muchas opciones valiosas: podés explorar ambas o combinarlas '
        'en tu recorrido académico.'
    )

    # ── Mapa de intereses (ordenado de mayor a menor) ──
    max_pts = ordenado[0][1] if ordenado else 1
    mapa_intereses = []
    for area, pts in ordenado:
        pct = int(pts / max_pts * 100) if max_pts else 0
        mapa_intereses.append({
            'nombre': area,
            'puntaje': pts,
            'color': _area_color(area),
            'pct': pct,
        })
    nota_mapa = (
        'Las barras muestran tu afinidad relativa en cada área. La más larga es '
        'tu área con mayor cantidad de respuestas alineadas.'
    )

    # ── Metodología ──
    pasos_metodologia = [
        {
            'titulo': 'Respondé tus preferencias',
            'descripcion': 'Cada pregunta suma puntos a las áreas con las que vos '
                           'más te identificás.',
        },
        {
            'titulo': 'Contamos afinidades',
            'descripcion': 'Sumamos tus respuestas y ordenamos las áreas según la '
                           'cantidad de elecciones alineadas.',
        },
        {
            'titulo': 'Te sugerimos carreras',
            'descripcion': 'Relacionamos tu área líder con carreras del catálogo '
                           'para darte opciones para empezar a mirar.',
        },
    ]

    # ── Carreras sugeridas ──
    carreras_sugeridas = []
    for c in (carreras or []):
        carreras_sugeridas.append({
            'area': c.get('area_profesional') or area_principal,
            'nombre': c.get('nombre') or '',
            'descripcion': (c.get('descripcion') or c.get('a_que_se_dedica') or ''),
        })

    # ── Respuestas destacadas (primeras 4 con elección) ──
    respuestas_destacadas = []
    for i, r in enumerate(respuestas_detalle[:4], start=1):
        respuestas_destacadas.append({
            'numero': i,
            'pregunta': r.get('pregunta', ''),
            'respuesta': r.get('opcion', ''),
        })

    # ── Anexo: todas las respuestas ──
    todas_las_respuestas = []
    for i, r in enumerate(respuestas_detalle, start=1):
        area = r.get('area') or None
        todas_las_respuestas.append({
            'numero': i,
            'pregunta': r.get('pregunta', ''),
            'eleccion': r.get('opcion', ''),
            'area': area,
            'area_slug': _area_slug(area) if area else '',
        })

    # ── Próximos pasos ──
    proximos_pasos = [
        'Investigá las carreras sugeridas en la sección Carreras y mirá sus '
        'planes de estudio y campo laboral.',
        'Anotá tus dudas y hablalas con docentes, profesionales o la orientadora '
        'vocacional de tu escuela.',
        'Explorá el test varias veces: tus intereses pueden evolucionar con el '
        'tiempo y la experiencia.',
    ]
    if notas:
        proximos_pasos.insert(0, f'Seguí desarrollando tus notas personales: {notas}')

    # ── Contexto del template ──
    primer_nombre = (usuario.get('nombre') or '').strip().split(' ')[0]
    inicial = primer_nombre[:1].upper() if primer_nombre else 'U'
    contexto = {
        'usuario': {
            'nombre': (usuario.get('nombre') or '').strip(),
            'primer_nombre': primer_nombre,
            'inicial': inicial,
            'email': usuario.get('email') or '',
        },
        'resultado': {
            'fecha': fecha_str,
            'area_lider': area_principal,
            'descripcion': descripcion,
            'total_preguntas': total_preguntas,
            'carreras': carreras_sugeridas,
            'empate': empate,
            'top_areas': top_areas,
            'nota_empate': nota_empate,
            'mapa_intereses': mapa_intereses,
            'nota_mapa': nota_mapa,
            'pasos_metodologia': pasos_metodologia,
            'respuestas_destacadas': respuestas_destacadas,
            'proximos_pasos': proximos_pasos,
            'todas_las_respuestas': todas_las_respuestas,
        },
    }

    return contexto


def generar_pdf_resultado(resultado, usuario, carreras=None):
    """Genera un informe PDF profesional del resultado vocacional con WeasyPrint."""
    contexto = _construir_contexto(resultado, usuario, carreras)

    # Importación diferida: WeasyPrint exige Pango en el SO; al importarlo solo
    # cuando se genera un PDF, la app arranca igual si falta en el entorno.
    from weasyprint import HTML
    html = render_template('comprobante.html', **contexto)
    buffer = io.BytesIO()
    HTML(string=html).write_pdf(buffer)
    buffer.seek(0)
    return buffer


@bp.route('/resultado/<int:resultado_id>/pdf')
@requiere_login
def descargar_resultado_pdf(resultado_id):
    """Genera un informe PDF profesional del resultado vocacional del estudiante."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, t.fecha_realizacion
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE r.id = %s AND t.usuario_id = %s
    """, (resultado_id, g.user['id']))
    resultado = cursor.fetchone()

    if not resultado:
        flash('Resultado no encontrado.', 'danger')
        return redirect(url_for('vocacional.mis_resultados'))

    # Carreras recomendadas (misma búsqueda flexible en 3 niveles que ver_resultado).
    area = resultado['area_profesional_sugerida']
    cursor.execute(
        """SELECT c.* FROM carreras c
           LEFT JOIN carrera_areas ca ON ca.carrera_id = c.id
           WHERE c.area_profesional = %s OR ca.area = %s
           GROUP BY c.id LIMIT 6""",
        (area, area)
    )
    carreras_sugeridas = cursor.fetchall()
    if not carreras_sugeridas:
        cursor.execute(
            "SELECT * FROM carreras WHERE area_profesional LIKE %s LIMIT 6",
            (f"%{area}%",)
        )
        carreras_sugeridas = cursor.fetchall()
    if not carreras_sugeridas:
        cursor.execute("SELECT * FROM carreras LIMIT 6")
        carreras_sugeridas = cursor.fetchall()

    buffer = generar_pdf_resultado(resultado, g.user, carreras_sugeridas)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"informe-vocacional-{g.user['nombre'].replace(' ','-')}.pdf",
        mimetype='application/pdf'
    )


@bp.route('/mis-resultados')
@requiere_login
def mis_resultados():
    """Listado histórico de todos los tests realizados por el usuario."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.area_profesional_sugerida, t.fecha_realizacion,
               r.detalle
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        WHERE t.usuario_id = %s
        ORDER BY t.fecha_realizacion DESC
    """, (g.user['id'],))
    resultados = cursor.fetchall()
    for item in resultados:
        try:
            detalle_data = json.loads(item['detalle'])
            texto = detalle_data.get('texto', item['detalle'])
        except Exception:
            texto = item['detalle']
        # Seguridad contra None (si el JSON tiene "texto": null no romper).
        texto = texto or item['detalle'] or ''
        item['detalle_texto'] = texto if len(texto) <= 160 else texto[:160].rsplit(' ', 1)[0] + '…'
    return render_template('mis_resultados.html', resultados=resultados)


@bp.route('/resultado/actualizar/<int:resultado_id>', methods=['POST'])
@requiere_login
def actualizar_resultado(resultado_id):
    """Guarda las notas personales del usuario sobre un resultado (U de CRUD)."""
    notas_personales = request.form['notas_personales']

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE resultados r
        JOIN tests t ON r.test_id = t.id
        SET r.notas_personales = %s
        WHERE r.id = %s AND t.usuario_id = %s
    """, (notas_personales, resultado_id, g.user['id']))
    db.commit()
    flash('Tus notas han sido guardadas correctamente.', 'success')
    return redirect(url_for('vocacional.ver_resultado', resultado_id=resultado_id))
