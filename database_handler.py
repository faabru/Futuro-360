"""
Manejador de la base de datos MySQL.

Provee la conexión a MySQL y su ciclo de vida dentro de Flask:
- ``obtener_db()``   → devuelve una conexión por request (cacheada en ``g``).
- ``cerrar_db(e)``   → cierra la conexión al terminar el request.
- ``inicializar_app``→ registra el cierre automático de conexiones.

Patrón utilizado: una única conexión por petición, que evita abrir/cerrar
conexiones en cada consulta y previene errores de "connection lost".
"""

import mysql.connector
from flask import g

from config import Config


def _config_conexion(database=None):
    """Construye los parámetros de conexión a MySQL desde la configuración.

    - ``DB_PORT``: puerto de conexión; si no está definido usa 3306.
    - ``DB_SSL_CA``: si apunta a un certificado CA, habilita TLS/SSL con
      verificación REAL del certificado del servidor (Aiven). Se exige SSL
      (``ssl_disabled=False``) y verificación de la identidad del host contra
      el certificado (``ssl_verify_identity=True``), nunca ``ssl_disabled``
      ni verificación desactivada. Sin certificado se mantiene el
      comportamiento local actual (sin SSL).
    """
    config = {
        'host': Config.DB_HOST,
        'user': Config.DB_USER,
        'password': Config.DB_PASSWORD,
        'port': int(Config.DB_PORT or 3306),
    }
    if database is not None:
        config['database'] = database
    if Config.DB_SSL_CA:
        config['ssl_disabled'] = False
        config['ssl_ca'] = Config.DB_SSL_CA
        config['ssl_verify_identity'] = True
    return config


def obtener_db():
    """
    Devuelve la conexión activa a la base de datos.

    La primera llamada dentro de un request crea la conexión y la guarda en
    el objeto ``g`` de Flask. Las siguientes llamadas reutilizan la misma
    conexión, mejorando el rendimiento.
    """
    if 'db' not in g:
        g.db = mysql.connector.connect(**_config_conexion(Config.DB_NAME))
    return g.db


def asegurar_base_datos():
    """
    Crea la base de datos si no existe (con el nombre/configuración de
    `Config.DB_NAME`), conectando sin seleccionar base primero.

    Idempotente. Si MySQL no está disponible, lanza el error y el llamador
    decide si continuar (el arranque de la app es tolerante a fallos).

    Si el usuario no tiene permiso para crear la base (p. ej. un usuario
    administrado como en Aiven), el intento se registra en consola y NO
    detiene el arranque: si la base ya existe, el paso siguiente
    (``sincronizar_tablas``) asegura tablas y columnas dentro de ella.
    """
    conn = mysql.connector.connect(**_config_conexion())
    try:
        cur = conn.cursor()
        try:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f'[bd] No se pudo crear la base `{Config.DB_NAME}`: {e}')
        finally:
            cur.close()
    finally:
        conn.close()


def cerrar_db(e=None):
    """Cierra la conexión guardada en ``g`` al finalizar el request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def inicializar_app(app):
    """
    Configura el cierre automático de conexiones.

    Se llama desde la fábrica de la aplicación (``create_app``) para que Flask
    ejecute ``cerrar_db`` cuando termina el contexto de cada petición.
    """
    app.teardown_appcontext(cerrar_db)
