# rss_fetcher.py
# Sistema de noticias automáticas para Futuro 360
# Trae noticias educativas desde múltiples feeds RSS gratuitos
# con extracción de imágenes y categorización automática.

import feedparser
import mysql.connector
import os
import requests
from datetime import date
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# ═══════════════════════════════════════
# FUENTES RSS EDUCATIVAS — todas gratuitas
# ═══════════════════════════════════════
FUENTES_RSS = [
    # Educación general argentina
    {
        'url': 'https://www.infobae.com/feeds/rss/educacion/',
        'fuente': 'Infobae Educación',
        'categoria': 'Educación'
    },
    {
        'url': 'https://www.clarin.com/rss/educacion/',
        'fuente': 'Clarín Educación',
        'categoria': 'Educación'
    },
    {
        'url': 'https://www.pagina12.com.ar/rss/suplementos/universidad',
        'fuente': 'Página 12 Universidad',
        'categoria': 'Universidad'
    },
    # Tecnología y carreras del futuro
    {
        'url': 'https://www.infobae.com/feeds/rss/tecno/',
        'fuente': 'Infobae Tecnología',
        'categoria': 'Tecnología'
    },
    {
        'url': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada',
        'fuente': 'El País Tecnología',
        'categoria': 'Tecnología'
    },
    # Ciencia y salud
    {
        'url': 'https://www.infobae.com/feeds/rss/salud/',
        'fuente': 'Infobae Salud',
        'categoria': 'Salud'
    },
    {
        'url': 'https://www.clarin.com/rss/sociedad/ciencia/',
        'fuente': 'Clarín Ciencia',
        'categoria': 'Ciencias Naturales'
    },
    # Becas y oportunidades (Universia)
    {
        'url': 'https://noticias.universia.net.ar/rss',
        'fuente': 'Universia Argentina',
        'categoria': 'Becas y Oportunidades'
    },
    # Economía y negocios
    {
        'url': 'https://www.infobae.com/feeds/rss/economia/',
        'fuente': 'Infobae Economía',
        'categoria': 'Negocios'
    },
    # Cultura y humanidades
    {
        'url': 'https://www.infobae.com/feeds/rss/cultura/',
        'fuente': 'Infobae Cultura',
        'categoria': 'Humanidades'
    },
]

# Palabras clave para filtrar solo noticias relevantes para estudiantes
PALABRAS_CLAVE_RELEVANTES = [
    'universidad', 'facultad', 'carrera', 'beca', 'ingreso', 'estudiante',
    'egresado', 'título', 'profesional', 'licenciatura', 'ingeniería',
    'medicina', 'derecho', 'psicología', 'educación', 'tecnología',
    'programación', 'ciencia', 'investigación', 'tucumán', 'unt', 'utn',
    'salud', 'trabajo', 'empleo', 'innovación', 'startup', 'inteligencia artificial',
    'diseño', 'arquitectura', 'economía', 'administración', 'comunicación'
]


def obtener_conexion():
    """Conexión directa a MySQL (fuera del contexto Flask)"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'futuro360')
    )


def parsear_fecha(entry):
    """Parsear la fecha de publicación del feed"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            t = entry.published_parsed
            return date(t.tm_year, t.tm_mon, t.tm_mday)
    except Exception:
        pass
    return date.today()


def obtener_imagen_feed(entry):
    """Intentar extraer imagen directamente del feed RSS"""
    try:
        # Método 1: media:content
        if hasattr(entry, 'media_content') and entry.media_content:
            url = entry.media_content[0].get('url', '')
            if url and url.startswith('http'):
                return url

        # Método 2: enclosures (podcasts/imágenes adjuntas)
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enc in entry.enclosures:
                url = enc.get('url', '')
                if url and url.startswith('http') and any(
                    url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']
                ):
                    return url

        # Método 3: media:thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            url = entry.media_thumbnail[0].get('url', '')
            if url and url.startswith('http'):
                return url

        # Método 4: buscar <img> en el contenido HTML del summary
        contenido = ''
        if hasattr(entry, 'content') and entry.content:
            contenido = entry.content[0].get('value', '')
        elif hasattr(entry, 'summary'):
            contenido = entry.summary or ''

        if contenido:
            soup = BeautifulSoup(contenido, 'html.parser')
            img = soup.find('img')
            if img and img.get('src', '').startswith('http'):
                return img['src']

    except Exception:
        pass
    return None


def obtener_imagen_scraping(url_noticia, timeout=5):
    """
    Fallback: hacer scraping de la página de la noticia
    para extraer la imagen og:image (Open Graph).
    Solo se usa si el feed no trae imagen.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Futuro360Bot/1.0)'}
        resp = requests.get(url_noticia, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')

        # og:image es el estándar para imagen de previsualización
        og = soup.find('meta', property='og:image')
        if og and og.get('content', '').startswith('http'):
            return og['content']

        # Fallback: twitter:image
        tw = soup.find('meta', attrs={'name': 'twitter:image'})
        if tw and tw.get('content', '').startswith('http'):
            return tw['content']

    except Exception:
        pass
    return None


def es_relevante(titulo, descripcion):
    """
    Verifica si la noticia es relevante para estudiantes
    buscando palabras clave en el título o descripción.
    """
    texto = (titulo + ' ' + descripcion).lower()
    return any(kw in texto for kw in PALABRAS_CLAVE_RELEVANTES)


def limpiar_html(texto):
    """Eliminar tags HTML del texto"""
    if not texto:
        return ''
    try:
        soup = BeautifulSoup(texto, 'html.parser')
        return soup.get_text(separator=' ').strip()
    except Exception:
        return texto


def actualizar_noticias_rss(max_por_fuente=8, scraping_imagen=True):
    """
    Recorre todos los feeds RSS, filtra noticias relevantes
    y las guarda en MySQL evitando duplicados.

    Args:
        max_por_fuente: máximo de noticias a procesar por feed
        scraping_imagen: si True, hace scraping para obtener imágenes cuando el feed no las trae
    """
    db = obtener_conexion()
    cursor = db.cursor()
    insertadas = 0
    filtradas = 0
    errores = 0

    print(f"=== Actualizando noticias — {len(FUENTES_RSS)} fuentes ===")

    for fuente_config in FUENTES_RSS:
        url_feed = fuente_config['url']
        fuente = fuente_config['fuente']
        categoria = fuente_config['categoria']

        try:
            print(f"\n-> Leyendo: {fuente}")
            feed = feedparser.parse(url_feed)

            if not feed.entries:
                print(f"  Sin entradas en el feed.")
                continue

            procesadas = 0
            for entry in feed.entries:
                if procesadas >= max_por_fuente:
                    break

                titulo = limpiar_html(entry.get('title', '')).strip()[:300]
                descripcion = limpiar_html(entry.get('summary', '')).strip()[:600]
                link = entry.get('link', '').strip()[:500]

                if not titulo or not link:
                    continue

                # Filtrar solo noticias relevantes para estudiantes
                if not es_relevante(titulo, descripcion):
                    filtradas += 1
                    continue

                fecha = parsear_fecha(entry)

                # Intentar obtener imagen del feed primero
                imagen = obtener_imagen_feed(entry)

                # Si no hay imagen en el feed, hacer scraping (opcional)
                if not imagen and scraping_imagen and link.startswith('http'):
                    imagen = obtener_imagen_scraping(link)

                try:
                    cursor.execute("""
                        INSERT IGNORE INTO noticias
                        (titulo, descripcion, imagen, fuente, fecha, link, categoria, es_externa)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                    """, (titulo, descripcion, imagen, fuente, fecha, link, categoria))

                    if cursor.rowcount > 0:
                        insertadas += 1
                        print(f"  + {titulo[:60]}...")
                    
                    procesadas += 1

                except Exception as e:
                    errores += 1
                    print(f"  ERROR insert: {e}")

        except Exception as e:
            print(f"  ERROR feed {url_feed}: {e}")

    db.commit()
    cursor.close()
    db.close()

    print(f"\n=== RESULTADO ===")
    print(f"  Insertadas:  {insertadas}")
    print(f"  Filtradas:   {filtradas} (no relevantes para estudiantes)")
    print(f"  Errores:     {errores}")
    return insertadas


if __name__ == "__main__":
    actualizar_noticias_rss()
