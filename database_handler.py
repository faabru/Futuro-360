"""
Manejador de la base de datos MySQL.

Una conexión por request (cacheada en ``g``), cerrada automáticamente.
Aiven free tier: ~10 conexiones max; gunicorn 2 workers → no se supera.
"""

import mysql.connector
from flask import g

from config import Config

def _config_conexion(database=None):
    """Parámetros de conexión a MySQL. DB_SSL_CA habilita TLS con verificación."""
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
    """Devuelve la conexión activa (creada en la 1ra llamada del request)."""
    if 'db' not in g:
        g.db = mysql.connector.connect(**_config_conexion(Config.DB_NAME))
    return g.db

def asegurar_base_datos():
    """Crea la BD si no existe. Idempotente. Si no hay permiso, solo avisa."""
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
    """Registra el cierre automático de conexiones al finalizar cada request."""
    app.teardown_appcontext(cerrar_db)
