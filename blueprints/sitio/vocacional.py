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
from datetime import datetime

from flask import (Blueprint, Response, current_app, flash, g, redirect,
                   render_template, request, send_file, url_for)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (HRFlowable, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

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
def generar_pdf_resultado(resultado, usuario):
    """
    Genera un informe PDF profesional del resultado del test vocacional.
    Diseño moderno con cabecera de color, secciones bien definidas y tipografía limpia.
    """
    buffer = io.BytesIO()

    # ── Configuración del documento ──
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=f"Informe Vocacional — {usuario['nombre']}",
        author="Futuro 360",
        subject="Resultado del Test Vocacional"
    )

    # ── Paleta de colores ──
    AZUL_PRIMARIO   = colors.HexColor('#1a56db')   # azul principal
    AZUL_OSCURO     = colors.HexColor('#1e3a5f')   # encabezado
    AZUL_CLARO      = colors.HexColor('#e8f0fe')   # fondo suave
    GRIS_TEXTO      = colors.HexColor('#374151')   # texto principal
    GRIS_SUAVE      = colors.HexColor('#6b7280')   # texto secundario
    VERDE_EXITO     = colors.HexColor('#059669')   # destacado positivo
    BLANCO          = colors.white

    # ── Estilos ──
    styles = getSampleStyleSheet()

    estilo_nombre = ParagraphStyle(
        'nombre', fontSize=22, fontName='Helvetica-Bold',
        textColor=BLANCO, alignment=TA_LEFT, leading=28
    )
    estilo_subtitulo_header = ParagraphStyle(
        'subtitulo_header', fontSize=11, fontName='Helvetica',
        textColor=colors.HexColor('#bfdbfe'), alignment=TA_LEFT, leading=16
    )
    estilo_area = ParagraphStyle(
        'area', fontSize=28, fontName='Helvetica-Bold',
        textColor=AZUL_PRIMARIO, alignment=TA_CENTER, leading=36
    )
    estilo_seccion = ParagraphStyle(
        'seccion', fontSize=13, fontName='Helvetica-Bold',
        textColor=AZUL_OSCURO, alignment=TA_LEFT, leading=18,
        spaceBefore=12, spaceAfter=6
    )
    estilo_cuerpo = ParagraphStyle(
        'cuerpo', fontSize=10, fontName='Helvetica',
        textColor=GRIS_TEXTO, alignment=TA_LEFT, leading=16
    )
    estilo_nota = ParagraphStyle(
        'nota', fontSize=9, fontName='Helvetica-Oblique',
        textColor=GRIS_SUAVE, alignment=TA_LEFT, leading=14
    )
    estilo_pie = ParagraphStyle(
        'pie', fontSize=8, fontName='Helvetica',
        textColor=GRIS_SUAVE, alignment=TA_CENTER, leading=12
    )

    # ── Parsear el desglose de puntajes ──
    puntajes = {}
    try:
        import json as _json
        detalle_data = _json.loads(resultado.get('detalle', '{}'))
        detalle_texto = detalle_data.get('texto', '')
        # Extraer puntajes del texto "Área: N pts"
        import re
        matches = re.findall(r'([^:,]+):\s*(\d+)\s*pts', detalle_texto)
        puntajes = {m[0].strip(): int(m[1]) for m in matches}
    except Exception:
        pass

    area_principal = resultado.get('area_profesional_sugerida', 'Sin determinar')
    notas = resultado.get('notas_personales', '')
    fecha_test = resultado.get('fecha_realizacion', datetime.now())
    if hasattr(fecha_test, 'strftime'):
        fecha_str = fecha_test.strftime('%d de %B de %Y')
    else:
        fecha_str = str(fecha_test)

    # ── Contenido del PDF ──
    elementos = []

    # ╔══════════════════════════════╗
    # ║  CABECERA con fondo azul     ║
    # ╚══════════════════════════════╝
    datos_header = [
        [
            Paragraph("Futuro 360", estilo_nombre),
            Paragraph(f"Fecha: {fecha_str}", ParagraphStyle(
                'fecha', fontSize=9, fontName='Helvetica',
                textColor=colors.HexColor('#bfdbfe'), alignment=TA_RIGHT
            ))
        ],
        [
            Paragraph("Informe de Orientación Vocacional", estilo_subtitulo_header),
            ''
        ],
        [
            Paragraph(f"Estudiante: {usuario.get('nombre', '')}", ParagraphStyle(
                'est', fontSize=10, fontName='Helvetica',
                textColor=BLANCO, alignment=TA_LEFT
            )),
            ''
        ],
    ]
    tabla_header = Table(datos_header, colWidths=[13*cm, 4*cm])
    tabla_header.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,-1), AZUL_OSCURO),
        ('TEXTCOLOR',   (0,0), (-1,-1), BLANCO),
        ('TOPPADDING',  (0,0), (-1,-1), 16),
        ('BOTTOMPADDING',(0,-1),(-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING',(0,0), (-1,-1), 16),
        ('ROUNDEDCORNERS', [8]),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
    ]))
    elementos.append(tabla_header)
    elementos.append(Spacer(1, 0.5*cm))

    # ╔══════════════════════════════╗
    # ║  ÁREA PRINCIPAL DESTACADA    ║
    # ╚══════════════════════════════╝
    tabla_area = Table(
        [[Paragraph("Área de Mayor Afinidad", ParagraphStyle(
            'lbl', fontSize=10, fontName='Helvetica',
            textColor=AZUL_PRIMARIO, alignment=TA_CENTER
          ))],
         [Paragraph(area_principal, estilo_area)],
         [Paragraph(
            "Esta es el área profesional con mayor afinidad según tus respuestas.",
            ParagraphStyle('sub', fontSize=9, fontName='Helvetica',
            textColor=GRIS_SUAVE, alignment=TA_CENTER)
          )]],
        colWidths=[17*cm]
    )
    tabla_area.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), AZUL_CLARO),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,-1),(-1,-1), 14),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [8]),
    ]))
    elementos.append(tabla_area)
    elementos.append(Spacer(1, 0.4*cm))

    # ╔══════════════════════════════╗
    # ║  DESGLOSE DE PUNTAJES        ║
    # ╚══════════════════════════════╝
    if puntajes:
        elementos.append(Paragraph("Desglose por área", estilo_seccion))
        elementos.append(HRFlowable(width="100%", thickness=1,
                                     color=AZUL_CLARO, spaceAfter=8))

        max_puntaje = max(puntajes.values()) if puntajes else 1
        filas_puntajes = []

        for area, pts in sorted(puntajes.items(), key=lambda x: x[1], reverse=True):
            porcentaje = int((pts / max_puntaje) * 100)
            es_principal = area == area_principal

            # Barra de progreso como tabla anidada
            barra_llena  = int(porcentaje * 0.10)  # max 10 celdas
            barra_vacia  = 10 - barra_llena

            celdas_barra = ([['']*barra_llena + ['']*barra_vacia])
            barra = Table(celdas_barra, colWidths=[0.8*cm]*10, rowHeights=[0.35*cm])
            estilo_barra = [
                ('BACKGROUND', (0,0), (barra_llena-1, 0), AZUL_PRIMARIO if not es_principal else VERDE_EXITO),
                ('BACKGROUND', (barra_llena,0), (-1,0), colors.HexColor('#e5e7eb')),
                ('ROUNDEDCORNERS', [4]),
                ('LEFTPADDING',  (0,0),(-1,-1), 0),
                ('RIGHTPADDING', (0,0),(-1,-1), 1),
                ('TOPPADDING',   (0,0),(-1,-1), 0),
                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
            ]
            barra.setStyle(TableStyle(estilo_barra))

            nombre_estilo = ParagraphStyle(
                'an', fontSize=10,
                fontName='Helvetica-Bold' if es_principal else 'Helvetica',
                textColor=VERDE_EXITO if es_principal else GRIS_TEXTO
            )
            pts_estilo = ParagraphStyle(
                'pts', fontSize=10, fontName='Helvetica-Bold',
                textColor=AZUL_PRIMARIO, alignment=TA_RIGHT
            )

            filas_puntajes.append([
                Paragraph(f"{'★ ' if es_principal else ''}{area}", nombre_estilo),
                barra,
                Paragraph(f"{pts} pts", pts_estilo)
            ])

        tabla_puntajes = Table(filas_puntajes, colWidths=[6*cm, 8.5*cm, 2.5*cm])
        tabla_puntajes.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [BLANCO, colors.HexColor('#f9fafb')]),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('RIGHTPADDING',  (0,0), (-1,-1), 8),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW',     (0,0), (-1,-2), 0.5, colors.HexColor('#e5e7eb')),
        ]))
        elementos.append(tabla_puntajes)
        elementos.append(Spacer(1, 0.4*cm))

    # ╔══════════════════════════════╗
    # ║  NOTAS PERSONALES            ║
    # ╚══════════════════════════════╝
    if notas and notas.strip():
        elementos.append(Paragraph("Mis notas personales", estilo_seccion))
        elementos.append(HRFlowable(width="100%", thickness=1,
                                     color=AZUL_CLARO, spaceAfter=8))
        tabla_notas = Table(
            [[Paragraph(notas, estilo_cuerpo)]],
            colWidths=[17*cm]
        )
        tabla_notas.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
            ('TOPPADDING',    (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING',   (0,0), (-1,-1), 14),
            ('RIGHTPADDING',  (0,0), (-1,-1), 14),
            ('ROUNDEDCORNERS', [6]),
        ]))
        elementos.append(tabla_notas)
        elementos.append(Spacer(1, 0.4*cm))

    # ╔══════════════════════════════╗
    # ║  PRÓXIMOS PASOS              ║
    # ╚══════════════════════════════╝
    elementos.append(Paragraph("¿Qué sigue?", estilo_seccion))
    elementos.append(HRFlowable(width="100%", thickness=1,
                                 color=AZUL_CLARO, spaceAfter=8))

    pasos = [
        ("1", "Explorá las carreras del área en el catálogo de Futuro 360."),
        ("2", "Usá el buscador por carrera para ver universidades en Tucumán."),
        ("3", "Consultá los requisitos de ingreso de cada facultad."),
        ("4", "Si tenés dudas, repetí el test en otro momento para comparar resultados."),
    ]
    for num, texto in pasos:
        fila = Table([[
            Paragraph(num, ParagraphStyle('num', fontSize=11, fontName='Helvetica-Bold',
                      textColor=BLANCO, alignment=TA_CENTER)),
            Paragraph(texto, estilo_cuerpo)
        ]], colWidths=[0.8*cm, 16.2*cm])
        fila.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (0,0), AZUL_PRIMARIO),
            ('TOPPADDING',    (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [4]),
        ]))
        elementos.append(fila)
        elementos.append(Spacer(1, 0.2*cm))

    # ╔══════════════════════════════╗
    # ║  PIE DE PÁGINA               ║
    # ╚══════════════════════════════╝
    elementos.append(Spacer(1, 0.6*cm))
    elementos.append(HRFlowable(width="100%", thickness=0.5, color=AZUL_CLARO))
    elementos.append(Spacer(1, 0.2*cm))
    elementos.append(Paragraph(
        f"Futuro 360 · Plataforma de Orientación Vocacional · Tucumán, Argentina · "
        f"futuro-360.onrender.com · {datetime.now().strftime('%Y')}",
        estilo_pie
    ))
    elementos.append(Paragraph(
        "Este informe es orientativo y no reemplaza el asesoramiento profesional.",
        estilo_pie
    ))

    # ── Construir el PDF ──
    doc.build(elementos)
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

    buffer = generar_pdf_resultado(resultado, g.user)

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
