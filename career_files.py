"""Gestión de archivos HTML por carrera en la carpeta carreras/"""
import json
import re
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).parent
CARRERAS_DIR = BASE_DIR / 'carreras'
STATIC_CARRERAS_DIR = BASE_DIR / 'static' / 'carreras'

META_PATTERN = re.compile(r'<!--\s*meta\s*(.*?)\s*-->', re.DOTALL | re.IGNORECASE)


def slugify(nombre):
    s = unicodedata.normalize('NFKD', nombre)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s or 'carrera'


def asegurar_carpetas():
    CARRERAS_DIR.mkdir(exist_ok=True)
    STATIC_CARRERAS_DIR.mkdir(exist_ok=True)


def ruta_html(slug):
    return CARRERAS_DIR / f'{slug}.html'


def url_imagen(imagen_nombre):
    if not imagen_nombre:
        return '/static/carreras/placeholder.svg'
    return f'/static/carreras/{imagen_nombre}'


def parsear_archivo(contenido):
    meta = {}
    cuerpo = contenido
    match = META_PATTERN.search(contenido)
    if match:
        try:
            meta = json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            meta = {}
        cuerpo = contenido[match.end():].strip()
    return meta, cuerpo


def cargar_carrera_html(carrera_id, nombre):
    asegurar_carpetas()
    slug = slugify(nombre)
    path = ruta_html(slug)
    if not path.exists():
        for f in CARRERAS_DIR.glob('*.html'):
            meta, _ = parsear_archivo(f.read_text(encoding='utf-8'))
            if meta.get('id') == carrera_id:
                path = f
                slug = meta.get('slug', f.stem)
                break
        else:
            return {
                'slug': slug,
                'imagen': '',
                'imagen_url': url_imagen(''),
                'cuerpo_html': '',
                'perfil': '',
            }

    contenido = path.read_text(encoding='utf-8')
    meta, cuerpo = parsear_archivo(contenido)
    imagen = meta.get('imagen', '')
    return {
        'slug': meta.get('slug', slug),
        'imagen': imagen,
        'imagen_url': url_imagen(imagen),
        'cuerpo_html': cuerpo,
        'perfil': meta.get('perfil', ''),
        'meta': meta,
    }


def guardar_carrera_html(carrera_id, nombre, area_profesional, descripcion, perfil='', imagen=''):
    asegurar_carpetas()
    slug = slugify(nombre)
    meta = {
        'id': carrera_id,
        'slug': slug,
        'nombre': nombre,
        'area_profesional': area_profesional,
        'imagen': imagen,
        'perfil': perfil,
    }
    perfil_html = perfil.strip() if perfil else descripcion
    cuerpo = f"""<p class="lead career-descripcion">{descripcion}</p>
<div class="career-perfil mb-4">
  <h5 class="fw-bold mb-3"><i class="bi bi-briefcase text-primary me-2"></i> ¿A qué se dedica?</h5>
  <p class="text-muted small">{perfil_html}</p>
</div>"""
    contenido = f"<!-- meta\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n-->\n{cuerpo}\n"
    ruta_html(slug).write_text(contenido, encoding='utf-8')
    return slug


def generar_desde_db(cursor):
    """Genera archivos HTML para todas las carreras de la BD que aún no existen."""
    asegurar_carpetas()
    cursor.execute("SELECT id, nombre, area_profesional, descripcion FROM carreras ORDER BY id")
    carreras = cursor.fetchall()
    creados = 0
    for c in carreras:
        slug = slugify(c['nombre'])
        path = ruta_html(slug)
        if path.exists():
            continue
        guardar_carrera_html(
            c['id'], c['nombre'], c['area_profesional'],
            c['descripcion'] or '', c['descripcion'] or ''
        )
        creados += 1
    return creados
