"""
Subidas de archivos (imágenes y videos) con Cloudinary.

Centraliza el guardado de las imágenes y videos del panel:

- Si Cloudinary está configurado (.env con CLOUDINARY_*), el archivo se sube
  a la nube y se devuelve su URL pública (≈ compartida entre máquinas).
- Si no, se guarda localmente en ``static/imagenes/`` y se devuelve la ruta
  relativa (comportamiento original, útil para desarrollo sin internet).
"""

import os
import time

from flask import current_app
from werkzeug.utils import secure_filename

from config import Config, EXTENSIONES_IMAGEN, EXTENSIONES_VIDEO


def cloudinary_configurado():
    """True si hay credenciales de Cloudinary definidas en el entorno."""
    return bool(Config.CLOUDINARY_CLOUD_NAME
                and Config.CLOUDINARY_API_KEY
                and Config.CLOUDINARY_API_SECRET)


def _configurar_cloudinary():
    """Configura el SDK de Cloudinary (idempotente).

    Se fija un timeout acotado para las llamadas a la API: si Cloudinary está
    lento o inaccesible, la subida no bloquea el request durante mucho tiempo y
    se cae rápido al guardado local (evita la "demora" al crear carreras con
    imágenes/videos).
    """
    if not getattr(_configurar_cloudinary, '_listo', False):
        import cloudinary as cloud
        cloud.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET,
            secure=True,
        )
        # Timeout de la API (segundos). Config soporta `api_request_timeout`
        # en versiones recientes; si no, se ignora con try/except.
        try:
            cloud.config(api_request_timeout=60)
        except Exception:
            pass
        _configurar_cloudinary._listo = True


def guardar_archivo(archivo, prefijo, carpeta='', es_video=False):
    """
    Guarda un archivo subido (imagen o video) en Cloudinary o localmente.

    - ``prefijo``: prefijo del nombre (ej: 'carrera', 'noticia').
    - ``carpeta``: subcarpeta dentro de static/imagenes y/o carpeta pública
      de Cloudinary (ej: 'noticias').
    - ``es_video``: valida contra extensiones de video en vez de imagen.
    Devuelve la URL (Cloudinary) o la ruta relativa (local), o None.
    """
    if archivo is None or not getattr(archivo, 'filename', ''):
        return None

    nombre_original = secure_filename(archivo.filename)
    if not nombre_original:
        return None

    ext = nombre_original.rsplit('.', 1)[-1].lower() if '.' in nombre_original else ''
    extensiones = EXTENSIONES_VIDEO if es_video else EXTENSIONES_IMAGEN
    if ext not in extensiones:
        return None

    nombre_unico = f"{prefijo}_{int(time.time())}_{nombre_original}"

    if cloudinary_configurado():
        # Un reintento: los fallos transitorios de red/Cloudinary suelen ser
        # pasajeros y no conviene caer al guardado local (que no persiste en
        # Render) si se puede subir a la nube.
        import cloudinary.uploader
        for intento in range(2):
            try:
                _configurar_cloudinary()
                resultado = cloudinary.uploader.upload(
                    archivo,
                    folder=carpeta or None,
                    public_id=os.path.splitext(nombre_unico)[0],
                    resource_type='video' if es_video else 'image',
                )
                return resultado.get('secure_url')
            except Exception as e:
                if intento == 0:
                    # Reintenta una vez; si vuelve a fallar, guarda local.
                    archivo.seek(0)  # resetea el stream antes del reintento
                    current_app.logger.warning(
                        'Cloudinary falló (intento %d): %s. Reintentando...',
                        intento + 1, e)
                else:
                    # Log con traceback completo para ver en Render el error
                    # exacto de Cloudinary (credenciales, versión, red, etc.).
                    current_app.logger.exception(
                        'Cloudinary no disponible tras %d intentos (config: '
                        'cloud=%s, key=%s). Guardando local. Error: %s',
                        intento + 1,
                        Config.CLOUDINARY_CLOUD_NAME,
                        Config.CLOUDINARY_API_KEY,
                        e)

    # Fallback local: mismo comportamiento que antes de Cloudinary.
    # Crear SIEMPRE static/imagenes (y la subcarpeta si corresponde) antes de
    # guardar: si la carpeta no existe, archivo.save() lanza FileNotFoundError
    # y rompe el alta de carreras/noticias con 500.
    base = os.path.join(current_app.static_folder, 'imagenes')
    os.makedirs(base, exist_ok=True)
    if carpeta:
        base = os.path.join(base, carpeta)
        os.makedirs(base, exist_ok=True)
    ruta = os.path.join(base, nombre_unico)
    archivo.save(ruta)
    ruta_relativa = f"imagenes/{carpeta}/{nombre_unico}" if carpeta else f"imagenes/{nombre_unico}"
    return ruta_relativa