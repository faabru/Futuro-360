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
    """Configura el SDK de Cloudinary (idempotente)."""
    if not getattr(_configurar_cloudinary, '_listo', False):
        import cloudinary as cloud
        cloud.config(
            cloud_name=Config.CLOUDINARY_CLOUD_NAME,
            api_key=Config.CLOUDINARY_API_KEY,
            api_secret=Config.CLOUDINARY_API_SECRET,
            secure=True,
        )
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
        try:
            _configurar_cloudinary()
            import cloudinary.uploader
            resultado = cloudinary.uploader.upload(
                archivo,
                folder=carpeta or None,
                public_id=os.path.splitext(nombre_unico)[0],
                resource_type='video' if es_video else 'image',
            )
            return resultado.get('secure_url')
        except Exception as e:
            # Si Cloudinary rechaza la subida (credenciales, permisos, red),
            # seguimos funcionando guardando el archivo localmente.
            current_app.logger.warning(
                'Cloudinary no disponible: %s. Guardando local.', e)

    # Fallback local: mismo comportamiento que antes de Cloudinary.
    base = os.path.join(current_app.static_folder, 'imagenes')
    if carpeta:
        base = os.path.join(base, carpeta)
        os.makedirs(base, exist_ok=True)
    ruta = os.path.join(base, nombre_unico)
    archivo.save(ruta)
    ruta_relativa = f"imagenes/{carpeta}/{nombre_unico}" if carpeta else f"imagenes/{nombre_unico}"
    return ruta_relativa