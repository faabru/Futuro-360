"""Script de ejemplo: genera el comprobante PDF con datos de prueba.

Usa la MISMA ruta de datos que genera comprobantes en producción:
- importa _construir_contexto() desde blueprints/sitio/vocacional.py
- renderiza templates/comprobante.html

Uso:
    python render_ejemplo.py            # PDF + HTML (requiere Pango en el SO)
    python render_ejemplo.py --html     # solo renderiza el HTML (sin WeasyPrint)
"""

import io
import os
import sys

# Para que el script corra desde la raíz del repo sin instalar el paquete.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jinja2 import Environment, FileSystemLoader, select_autoescape

from blueprints.sitio.vocacional import _construir_contexto


def datos_ejemplo():
    """Resultado de prueba (área líder Arte y Diseño, empate y 30 respuestas)."""
    resultado = {
        'area_profesional_sugerida': 'Arte y Diseño',
        'notas_personales': '',
        'detalle': _detalle_json(),
        'fecha_realizacion': _FechaPrueba(1, 9, 2026),
    }
    usuario = {
        'nombre': 'Fabricio',
        'apellido': 'Perez',
        'email': 'fabricio@ejemplo.com',
    }
    carreras = [
        {'area_profesional': 'Arte y Diseño', 'nombre': 'Lic. en Diseño Gráfico',
         'descripcion': 'Diseño de piezas visuales y comunicación gráfica.'},
        {'area_profesional': 'Arte y Diseño', 'nombre': 'Arquitectura',
         'descripcion': 'Proyecto y construcción de espacios habitables.'},
        {'area_profesional': 'Humanidades', 'nombre': 'Lic. en Ciencias de la Comunicación',
         'descripcion': 'Estudia los procesos de comunicación y los medios.'},
        {'area_profesional': 'Arte y Diseño', 'nombre': 'Tecnicatura en Animación',
         'descripcion': 'Animación digital 2D/3D para cine, juegos y publicidad.'},
    ]
    return resultado, usuario, carreras


def _detalle_json():
    areas = ['Arte y Diseño', 'Humanidades', 'Salud', 'Negocios', 'Tecnología']
    respuestas = []
    for i in range(1, 31):
        respuestas.append({
            'pregunta': f'Actividad de la pregunta {i}',
            'opcion': f'Opción elegida {i}',
            'area': areas[i % len(areas)],
        })
    resumen = [
        {'area': 'Arte y Diseño', 'puntos': 12},
        {'area': 'Humanidades', 'puntos': 12},
        {'area': 'Salud', 'puntos': 3},
        {'area': 'Negocios', 'puntos': 2},
        {'area': 'Tecnología', 'puntos': 1},
    ]
    return __import__('json').dumps({
        'texto': 'Texto de ejemplo del detalle.',
        'resumen': resumen,
        'respuestas': respuestas,
    }, ensure_ascii=False)


class _FechaPrueba:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


def main():
    solo_html = '--html' in sys.argv
    resultado, usuario, carreras = datos_ejemplo()
    contexto = _construir_contexto(resultado, usuario, carreras)

    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')),
        autoescape=select_autoescape(['html']),
    )
    html = env.get_template('comprobante.html').render(**contexto)

    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comprobante_ejemplo.html')
    with io.open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('HTML generado:', html_path)

    if solo_html:
        return

    from weasyprint import HTML
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comprobante_ejemplo.pdf')
    HTML(string=html).write_pdf(pdf_path)
    print('PDF generado:', pdf_path)


if __name__ == '__main__':
    main()