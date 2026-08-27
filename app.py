"""
Punto de entrada de Futuro 360.
Construye la app Flask y arranca el servidor. Toda la lógica está en módulos.
"""

import time

from flask import Flask, g, render_template, session, url_for
from flask_wtf.csrf import CSRFProtect

from blueprints import registrar_blueprints
from config import Config
from core.startup import sincronizar_imagenes, sincronizar_juego, sincronizar_tablas
from database_handler import asegurar_base_datos, inicializar_app, obtener_db

# Protección CSRF global: token en todo POST/PUT/PATCH/DELETE.
csrf = CSRFProtect()


def create_app():
    """Fábrica de la aplicación Flask: configura y registra todo."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # CSRF + SAMESITE=Lax cubren el vector principal de CSRF.
    csrf.init_app(app)

    # Cierre automático de la conexión a MySQL al terminar cada request.
    inicializar_app(app)

    # Sincronizar esquema y contenido al arrancar (idempotente, tolerante a fallos).
    try:
        with app.app_context():
            asegurar_base_datos()
            sincronizar_tablas()
            sincronizar_juego()
    except Exception as e:
        print(f'[startup] No se pudo sincronizar la base de datos: {e}')

    # Todos los blueprints (sitio público + panel admin).
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
        """Carga en 'g.user' al usuario del sitio (si hay sesión) y registra la
        presencia 'en línea' tanto de usuarios del sitio como de administradores
        logueados en el panel."""
        id_usuario = session.get('user_id')
        if id_usuario is None:
            g.user = None
        else:
            db = obtener_db()
            cursor = db.cursor(dictionary=True)
            # SOLO columnas que la sesión necesita; sin password por seguridad.
            cursor.execute(
                "SELECT id, nombre, apellido, email, es_dueño FROM usuarios "
                "WHERE id = %s",
                (id_usuario,))
            g.user = cursor.fetchone()
            if g.user is None:
                return
            _registrar_presencia(id_usuario)
            return

        # Sin sesión de sitio: si hay sesión de administrador, registrar su
        # presencia para que también aparezca como "en línea" en el panel.
        if session.get('admin_autenticado'):
            _registrar_presencia(session.get('admin_id'))


    def _registrar_presencia(user_id):
        """Actualiza la presencia 'en línea' en sesiones_activas (máx 1 escritura/60s).
        Se usa para usuarios del sitio y para administradores del panel; así el
        indicador de "en línea" del panel refleja también a los admins conectados."""
        if not user_id:
            return
        ahora = time.time()
        if ahora - session.get('_online_ts', 0) <= 60:
            return
        session['_online_ts'] = ahora
        try:
            db = obtener_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO sesiones_activas (user_id, last_seen) "
                "VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE last_seen = NOW()",
                (user_id,))
            # TRADE-OFF: DELETE de sesiones viejas en cada request activo.
            # Simple y suficiente para el tráfico actual. Si crece, mover
            # a job periódico (APScheduler/CRON).
            cursor.execute(
                "DELETE FROM sesiones_activas WHERE last_seen < NOW() - INTERVAL 5 MINUTE")
            db.commit()
        except Exception:
            # Si la tabla no existe, crearla y reintentar una vez.
            try:
                from core.migraciones import asegurar_tabla_sesiones_activas
                asegurar_tabla_sesiones_activas()
                db = obtener_db()
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO sesiones_activas (user_id, last_seen) "
                    "VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE last_seen = NOW()",
                    (user_id,))
                cursor.execute(
                    "DELETE FROM sesiones_activas WHERE last_seen < NOW() - INTERVAL 5 MINUTE")
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


# Instancia global para el servidor (flask run, gunicorn, etc.).
app = create_app()


if __name__ == '__main__':
    print("=== INICIANDO FUTURO 360 ===")
    with app.app_context():
        print("Sincronizando imágenes...")
        sincronizar_imagenes()
        print("Listo. Iniciando servidor...")
    # debug=False en producción (gunicorn ignora este flag).
    app.run(debug=False)
