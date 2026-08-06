"""
Rutas del test vocacional y sus resultados (R del CRUD de Resultados).

- ``test``                  → pantalla del test y POST que calcula y guarda.
- ``ver_resultado``         → detalle de un resultado específico.
- ``descargar_resultado_pdf``→ informe PDF profesional (mejora TFI).
- ``mis_resultados``        → histórico de todos los tests del usuario.
- ``actualizar_resultado``  → guarda las notas personales de un resultado.
"""

import io
import json
import re
import traceback

from flask import (Blueprint, Response, flash, g, redirect, render_template,
                   request, url_for)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from core.decoradores import requiere_login
from database_handler import obtener_db

bp = Blueprint('vocacional', __name__)


@bp.route('/test', methods=['GET', 'POST'])
@requiere_login
def test():
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        puntuacion = {}
        for key in request.form.keys():
            if key.startswith('q_') or key.isdigit():
                areas = request.form.getlist(key)
                for area in areas:
                    area_limpia = area.strip() if area else ''
                    # Ignorar valores nulos, vacíos, 'Neutral' o 'Ninguna de las
                    # anteriores' — no suman puntos.
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

        # Construir detalle descriptivo como JSON válido (requerido por la BD,
        # la columna tiene CHECK(json_valid)).
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
            flash(f'¡Test completado! Tu área principal es: {area_ganadora}.', 'success')
            return redirect(url_for('vocacional.ver_resultado', resultado_id=resultado_id))

        except Exception as e:
            traceback.print_exc()
            db.rollback()
            flash(f'Error al guardar: {str(e)}', 'danger')
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


# --- INFORME PDF DEL RESULTADO VOCACIONAL (mejora TFI: reportes en PDF) ---
@bp.route('/resultado/<int:resultado_id>/pdf')
@requiere_login
def descargar_resultado_pdf(resultado_id):
    """Genera un informe PDF profesional del resultado vocacional del estudiante."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, t.fecha_realizacion, u.nombre, u.apellido, u.email
        FROM resultados r
        JOIN tests t ON r.test_id = t.id
        JOIN usuarios u ON t.usuario_id = u.id
        WHERE r.id = %s AND t.usuario_id = %s
    """, (resultado_id, g.user['id']))
    resultado = cursor.fetchone()

    if not resultado:
        flash('No se pudo encontrar el resultado solicitado.', 'danger')
        return redirect(url_for('vocacional.mis_resultados'))

    # Interpretar el detalle (misma lógica que la vista del resultado).
    detalle_texto = resultado['detalle'] or ''
    resumen_puntuacion = []
    try:
        detalle_data = json.loads(detalle_texto)
        detalle_texto = detalle_data.get('texto', detalle_texto)
        resumen_puntuacion = detalle_data.get('resumen', [])
    except Exception:
        pass
    if not resumen_puntuacion:
        partes = re.findall(r'([\w\s]+?):\s*(\d+)\s*pts', detalle_texto)
        resumen_puntuacion = [{"area": a.strip(), "puntos": int(p)} for a, p in partes]

    # Carreras sugeridas para el área dominante.
    area = resultado['area_profesional_sugerida']
    cursor.execute(
        """SELECT c.nombre, c.area_profesional FROM carreras c
           LEFT JOIN carrera_areas ca ON ca.carrera_id = c.id
           WHERE c.area_profesional = %s OR ca.area = %s
           GROUP BY c.id LIMIT 6""",
        (area, area))
    carreras = cursor.fetchall()
    if not carreras:
        cursor.execute(
            "SELECT nombre, area_profesional FROM carreras WHERE area_profesional LIKE %s LIMIT 6",
            (f"%{area}%",))
        carreras = cursor.fetchall()

    # --- Construcción del PDF ---
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle('Titulo', parent=estilos['Title'], fontName='Helvetica-Bold',
                            fontSize=18, textColor=colors.HexColor('#142B38'), spaceAfter=4)
    subtitulo = ParagraphStyle('Subtitulo', parent=estilos['Normal'], fontName='Helvetica',
                               fontSize=11, textColor=colors.HexColor('#2F8EAB'), spaceAfter=2)
    cabecera = ParagraphStyle('Cabecera', parent=estilos['Normal'], fontName='Helvetica-Bold',
                              fontSize=9, textColor=colors.HexColor('#2F8EAB'), spaceAfter=8)
    normal = ParagraphStyle('Normal', parent=estilos['Normal'], fontName='Helvetica',
                            fontSize=10, leading=15, textColor=colors.HexColor('#1F2937'))
    seccion = ParagraphStyle('Seccion', parent=estilos['Heading2'], fontName='Helvetica-Bold',
                             fontSize=13, textColor=colors.HexColor('#142B38'), spaceBefore=16, spaceAfter=8)

    story = []
    story.append(Paragraph('FUTURO 360', titulo))
    story.append(Paragraph('Orientación Vocacional · Tucumán, Argentina', subtitulo))
    story.append(Spacer(1, 10))
    story.append(Paragraph('Informe del resultado vocacional', cabecera))
    story.append(Paragraph(f"<b>Estudiante:</b> {resultado['nombre'] or ''} {resultado['apellido'] or ''}",
                           normal))
    story.append(Paragraph(f"<b>Email:</b> {resultado['email']}", normal))
    fecha = resultado['fecha_realizacion']
    if hasattr(fecha, 'strftime'):
        fecha = fecha.strftime('%d/%m/%Y')
    story.append(Paragraph(f"<b>Fecha del test:</b> {fecha}", normal))
    story.append(Spacer(1, 12))

    # Área dominante (caja destacada).
    tbl_area = Table([[Paragraph(f"ÁREA PROFESIONAL DOMINANTE", cabecera),
                       Paragraph(f"<font color='#2F8EAB'><b>{area}</b></font>", normal)]],
                     colWidths=[100 * mm, 90 * mm])
    tbl_area.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF7FA')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2F8EAB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(tbl_area)

    # Interpretación.
    story.append(Paragraph('Interpretación del resultado', seccion))
    story.append(Paragraph(detalle_texto or 'Sin detalle disponible.', normal))

    # Afinidad por área.
    if resumen_puntuacion:
        story.append(Paragraph('Afinidad por área', seccion))
        total_pts = sum(float(i.get('puntos', 0) or 0) for i in resumen_puntuacion) or 1
        filas = [['Área', 'Puntos', 'Participación']]
        for i in resumen_puntuacion:
            pts = float(i.get('puntos', 0) or 0)
            pct = (pts / total_pts) * 100
            filas.append([str(i.get('area', '')), f"{pts:g}", f"{pct:.1f}%"])
        tbl = Table(filas, colWidths=[90 * mm, 50 * mm, 50 * mm])
        tbl.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#142B38')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F6F9')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D9E0')),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        story.append(tbl)

    # Carreras recomendadas.
    story.append(Paragraph('Carreras recomendadas', seccion))
    if carreras:
        for i, c in enumerate(carreras, 1):
            story.append(Paragraph(f"{i}. <b>{c['nombre']}</b> — {c['area_profesional']}", normal))
    else:
        story.append(Paragraph('Consultá el catálogo de carreras en la plataforma.', normal))

    # Notas personales.
    if resultado.get('notas_personales'):
        story.append(Paragraph('Notas personales', seccion))
        story.append(Paragraph(resultado['notas_personales'], normal))

    story.append(Spacer(1, 24))
    story.append(Paragraph('Informe generado por Futuro 360 · Orientación Vocacional',
                           ParagraphStyle('Footer', parent=estilos['Normal'], fontName='Helvetica',
                                          fontSize=8, textColor=colors.HexColor('#9CA3AF'))))

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm,
                            title='Informe Vocacional Futuro 360',
                            author='Futuro 360')
    doc.build(story)
    buf.seek(0)

    return Response(buf, mimetype='application/pdf', headers={
        'Content-Disposition': f'attachment; filename=resultado_vocacional_{resultado_id}.pdf'
    })


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
