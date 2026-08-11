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
(before_request y errores). Al ejecutar el archivo se inicia la sincronización
de imágenes (una sola vez) y luego el servidor de desarrollo.
"""

import time

from flask import Flask, g, render_template, session

from blueprints import registrar_blueprints
from config import Config
from core.startup import sincronizar_imagenes, sincronizar_juego, sincronizar_tablas
from database_handler import inicializar_app, obtener_db


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
            sincronizar_tablas()
            sincronizar_juego()
    except Exception as e:
        print(f'[startup] No se pudo sincronizar la base de datos: {e}')

    # Todos los blueprints (sitio público + panel admin) con sus rutas.
    registrar_blueprints(app)

    @app.before_request
    def cargar_usuario_logueado():
        """Carga en 'g.user' los datos del usuario con sesión activa."""
        id_usuario = session.get('user_id')
        if id_usuario is None:
            g.user = None
            return
        db = obtener_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
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
        return render_template(
            'base.html',
            content="<div class='container py-5 text-center'><h1>500</h1>"
                    "<p>Algo salió mal. Por favor, intenta más tarde.</p></div>"
        ), 500

    return app


# Instancia global usada por el servidor (flask run, gunicorn, etc.).
app = create_app()


if __name__ == '__main__':
    print("=== INICIANDO APLICACIÓN FLASK ===")
    with app.app_context():
        print("Asegurando tablas de la base de datos...")
        sincronizar_tablas()
        print("Ejecutando sincronización de imágenes...")
        sincronizar_imagenes()
        print("Sincronización completada. Iniciando servidor...")
        sincronizar_juego()
    app.run(debug=True)
