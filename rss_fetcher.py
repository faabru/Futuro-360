# rss_fetcher.py 
# Módulo para obtener noticias desde feeds RSS externos y guardarlas en MySQL 
import feedparser 
import mysql.connector 
import os 
from datetime import datetime, date 
from dotenv import load_dotenv 
  
load_dotenv() 
  
# Fuentes RSS de noticias educativas y universitarias 
FUENTES_RSS = [ 
    { 
        'url': 'https://www.universia.net/ar/actualidad/rss.xml', 
        'fuente': 'Universia', 
        'categoria': 'Universidad' 
    }, 
    { 
        'url': 'https://www.infobae.com/feeds/rss/educacion/', 
        'fuente': 'Infobae Educación', 
        'categoria': 'Educación' 
    }, 
] 
  
def obtener_conexion(): 
    """Obtener conexión directa a MySQL (fuera del contexto Flask)""" 
    return mysql.connector.connect( 
        host=os.getenv('DB_HOST', 'localhost'), 
        user=os.getenv('DB_USER', 'root'), 
        password=os.getenv('DB_PASSWORD', ''), 
        database=os.getenv('DB_NAME', 'futuro360') 
    ) 
  
def parsear_fecha(entry): 
    """Intentar parsear la fecha de una entrada RSS""" 
    try: 
        if hasattr(entry, 'published_parsed') and entry.published_parsed: 
            t = entry.published_parsed 
            return date(t.tm_year, t.tm_mon, t.tm_mday) 
    except: 
        pass 
    return date.today() 
  
def obtener_imagen(entry): 
    """Intentar extraer la imagen de una entrada RSS""" 
    try: 
        if hasattr(entry, 'media_content') and entry.media_content: 
            return entry.media_content[0].get('url', None) 
        if hasattr(entry, 'enclosures') and entry.enclosures: 
            return entry.enclosures[0].get('url', None) 
    except: 
        pass 
    return None 
  
def actualizar_noticias_rss(): 
    """ 
    Recorre los feeds RSS, lee las noticias y las guarda en MySQL. 
    Usa UNIQUE KEY en el campo link para evitar duplicados. 
    """ 
    db = obtener_conexion() 
    cursor = db.cursor() 
    insertadas = 0 
    errores = 0 
  
    for fuente_config in FUENTES_RSS: 
        try: 
            print(f"Leyendo RSS: {fuente_config['url']}") 
            feed = feedparser.parse(fuente_config['url']) 
  
            for entry in feed.entries[:10]:  # Máximo 10 por fuente 
                titulo = entry.get('title', '').strip()[:300] 
                descripcion = entry.get('summary', '').strip()[:500] 
                link = entry.get('link', '#').strip()[:500] 
                imagen = obtener_imagen(entry) 
                fecha = parsear_fecha(entry) 
                fuente = fuente_config['fuente'] 
                categoria = fuente_config['categoria'] 
  
                if not titulo: 
                    continue 
  
                try: 
                    cursor.execute(""" 
                        INSERT IGNORE INTO noticias  
                        (titulo, descripcion, imagen, fuente, fecha, link, categoria, es_externa) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 1) 
                    """, (titulo, descripcion, imagen, fuente, fecha, link, categoria)) 
                    if cursor.rowcount > 0: 
                        insertadas += 1 
                except Exception as e: 
                     errores += 1 
                     print(f"Error insertando noticia: {e}") 
  
        except Exception as e: 
            print(f"Error leyendo feed {fuente_config['url']}: {e}") 
  
    db.commit() 
    cursor.close() 
    db.close() 
    print(f"RSS actualizado: {insertadas} noticias nuevas, {errores} errores.") 
    return insertadas 
  
if __name__ == "__main__": 
    actualizar_noticias_rss() 
