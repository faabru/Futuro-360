"""
Migra a Cloudinary las imágenes que ya están guardadas localmente
(`static/imagenes/`) y actualiza las URLs en la base de datos.

Esto se hace UNA sola vez para que las imágenes existentes queden como URLs
compartidas (y tu compañera u otro despliegue puedan verlas también).

Requisitos:
    - Cloudinary configurado en el .env (CLOUDINARY_CLOUD_NAME / API_KEY /
      API_SECRET). Sin eso, el script avisa y no hace nada.

Uso:
    python scripts/migrar_imagenes_cloudinary.py
"""

import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

from config import Config  # noqa: E402


def configurar_cloudinary():
    import cloudinary as cloud
    cloud.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
        secure=True,
    )


def subir(archivo_local, public_id):
    import cloudinary.uploader
    if not os.path.exists(archivo_local):
        return None
    resultado = cloudinary.uploader.upload(
        archivo_local, public_id=public_id, resource_type='image')
    return resultado.get('secure_url')


def main():
    if not (Config.CLOUDINARY_CLOUD_NAME and Config.CLOUDINARY_API_KEY
            and Config.CLOUDINARY_API_SECRET):
        print('Cloudinary NO está configurado en el .env. Nada que migrar.')
        return

    configurar_cloudinary()
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'static', 'imagenes')

    db = mysql.connector.connect(
        host=Config.DB_HOST, user=Config.DB_USER, password=Config.DB_PASSWORD,
        database=Config.DB_NAME)
    cur = db.cursor(dictionary=True)

    total = 0

    def migrar_campo(tabla, fila, campo, columnas):
        nonlocal total
        valor = (fila.get(campo) or '').strip()
        if not valor.startswith('imagenes/'):
            return
        archivo_local = os.path.join(base, valor.replace('imagenes/', ''))
        if not os.path.exists(archivo_local):
            print(f'  [falta archivo] {tabla}.{campo} -> {archivo_local}')
            return
        public_id = os.path.splitext(os.path.basename(archivo_local.replace('\\', '/')))[0]
        url = subir(archivo_local, public_id)
        if not url:
            print(f'  [error subida] {tabla}.{campo} -> {archivo_local}')
            return
        cur.execute("UPDATE %s SET %s = %%s WHERE id = %%s" % (tabla, campo),
                    (url, fila['id']))
        total += 1
        print(f'  OK {tabla}.{campo} -> {url}')

    print('Migrando carreras...')
    cur.execute("SELECT * FROM carreras")
    for fila in cur.fetchall():
        for campo in ['imagen', 'imagen_portada', 'imagen_principal']:
            migrar_campo('carreras', fila, campo, [])

    print('Migrando noticias...')
    cur.execute("SELECT * FROM noticias")
    for fila in cur.fetchall():
        migrar_campo('noticias', fila, 'imagen', [])

    db.commit()
    print(f'\nListo: {total} imágenes migradas a Cloudinary.')


if __name__ == '__main__':
    main()