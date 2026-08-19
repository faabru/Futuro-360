"""
Punto de entrada de Futuro 360.

Este archivo queda reducido a su función esencial: construir la aplicación
Flask y arrancar el servidor. Toda la lógica está organizada en módulos:

- ``config.py``            → configuración central (BD, seguridad, email).
- ``database_handler.py``  → conexión a MySQL (una por request).
- ``core/``                → lógica transversal (decoradores, migraciones,
                            arranque, email).
- ``blueprints/``          → rutas del sitio público y del panel admin.

La fábrica ``create_app`` registra los blueprints y los manejadores globales
(before_request y errores). La instancia ``app`` se crea a nivel de módulo
para que cualquier servidor WSGI (``python app.py``, ``flask run``, gunicorn
vía ``Procfile``, waitress, etc.) la importe directamente.

En producción se sirve con **gunicorn** (ver ``Procfile``) y el arranque
directo con ``python app.py`` queda como modo de desarrollo con
``debug=False`` (no se expone el debugger de Werkzeug).
"""

import time

from flask import Flask, g, render_template, session, url_for

from blueprints import registrar_blueprints
from config import Config
from core.startup import sincronizar_imagenes, sincronizar_juego, sincronizar_tablas
from database_handler import asegurar_base_datos, inicializar_app, obtener_db


def create_app():
    """Fábrica de la aplicación Flask: configura y registra todo."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Cierre automático de la conexión a MySQL al terminar cada request.
    inicializar_app(app)

    # Asegura que el esquema de la BD esté completo (tablas, columnas y datos
    # iniciales) sin importar cómo se levante la app: `python app.py`,
    # `flask run`, gunicorn, waitress, etc. Es idempotente y tolerante a
    # fallos: si la BD no está disponible aún, el arranque continúa.
    try:
        with app.app_context():
            asegurar_base_datos()
            sincronizar_tablas()
            sincronizar_juego()
    except Exception as e:
        print(f'[startup] No se pudo sincronizar la base de datos: {e}')

    # Todos los blueprints (sitio público + panel admin) con sus rutas.
    registrar_blueprints(app)

    @app.template_filter('media')
    def media(valor):
        """Devuelve una URL de imagen/video lista para usar en <img>/<video>.
        Si el valor es una ruta local ('imagenes/...') genera la URL de static;
        si ya es una URL completa (https, Cloudinary), la devuelve tal cual."""
        if not valor:
            return ''
        if valor.startswith('imagenes/') or valor.startswith('static/'):
            return url_for('static', filename=valor)
        return valor

    @app.before_request
    def cargar_usuario_logueado():
        """Carga en 'g.user' los datos del usuario con sesión activa."""
        id_usuario = session.get('user_id')
        if id_usuario is None:
            g.user = None
            return
        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        # SOLO las columnas que la sesión necesita (base.html, dashboard,
        # perfil, decoradores, etc.). Se excluye 'password' para no traer el
        # hash a memoria en cada request.
        cursor.execute(
            "SELECT id, nombre, apellido, email, es_dueño FROM usuarios "
            "WHERE id = %s",
            (id_usuario,))
        g.user = cursor.fetchone()
        if g.user is None:
            return
        # Registrar actividad para el contador de "usuarios en línea".
        # Máximo una escritura por sesión cada 60s para no recargar la BD.
        ahora = time.time()
        if ahora - session.get('_online_ts', 0) > 60:
            session['_online_ts'] = ahora
            try:
                cursor.execute(
                    "INSERT INTO sesiones_activas (user_id, last_seen) "
                    "VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE last_seen = NOW()",
                    (id_usuario,))
                # TRADE-OFF: el DELETE de sesiones viejas se ejecuta en el
                # before_request de cada usuario activo (máx. 1 vez/60s por
                # usuario). Es simple y suficiente para el tráfico actual, pero
                # suma una escritura a la BD por cada request "heartbeat".
                # Si el tráfico crece, conviene mover esta limpieza a un job
                # periódico (APScheduler/CRON) que ejecute:
                #   DELETE FROM sesiones_activas
                #   WHERE last_seen < NOW() - INTERVAL 5 MINUTE
                # y dejar aquí solo el INSERT/UPDATE (ON DUPLICATE KEY).
                cursor.execute(
                    "DELETE FROM sesiones_activas "
                    "WHERE last_seen < NOW() - INTERVAL 5 MINUTE")
                db.commit()
            except Exception:
                # Si la tabla aún no existe (primera ejecución), la creamos
                # y reintentamos una vez.
                try:
                    from core.migraciones import asegurar_tabla_sesiones_activas
                    asegurar_tabla_sesiones_activas()
                    cursor.execute(
                        "INSERT INTO sesiones_activas (user_id, last_seen) "
                        "VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE last_seen = NOW()",
                        (id_usuario,))
                    cursor.execute(
                        "DELETE FROM sesiones_activas "
                        "WHERE last_seen < NOW() - INTERVAL 5 MINUTE")
                    db.commit()
                except Exception:
                    pass

    @app.errorhandler(404)
    def pagina_no_encontrada(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def error_interno(e):
        return render_template('500.html'), 500

    return app


# Instancia global usada por el servidor (flask run, gunicorn, etc.).
app = create_app()


if __name__ == '__main__':
    print("=== INICIANDO FUTURO 360 ===")
    with app.app_context():
        print("Sincronizando imágenes...")
        sincronizar_imagenes()
        print("Listo. Iniciando servidor...")
    # debug=False en producción para no exponer el debugger de Werkzeug.
    # Gunicorn ignora este flag, pero es buena práctica dejarlo en False.
    app.run(debug=False)
