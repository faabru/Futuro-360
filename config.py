"""
Configuración central de Futuro 360.
Credenciales, variables de entorno, constantes de dominio y opciones de Flask.
"""

import atexit
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (BD, secretos, emails, etc.).
# Si el archivo no existe, se usan los valores por defecto definidos abajo.
load_dotenv()


def _materializar_ca(contenido_pem):
    """Escribe un certificado CA (PEM) a un archivo temporal del sistema.
    Útil para Render/Railway donde el certificado llega por variable de entorno.
    Devuelve la ruta del archivo, o None si no es PEM válido."""
    if not contenido_pem:
        return None
    # Normaliza saltos de línea y elimina espacios/fin de línea sobrantes.
    pem = contenido_pem.strip().replace('\r\n', '\n').replace('\r', '\n') + '\n'
    if '-----BEGIN CERTIFICATE-----' not in pem or '-----END CERTIFICATE-----' not in pem:
        print("[config] DB_SSL_CA_CONTENT no parece un certificado PEM válido "
              "(faltan BEGIN/END CERTIFICATE). Conectando sin SSL.")
        return None

    archivo = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.pem',
        prefix='aiven-ca-',
        delete=False,
        encoding='utf-8',
    )
    try:
        archivo.write(pem)
        archivo.flush()
        os.fsync(archivo.fileno())
    finally:
        archivo.close()

    def _limpiar():
        try:
            if os.path.exists(archivo.name):
                os.unlink(archivo.name)
        except OSError:
            pass

    # Borrado seguro al finalizar el proceso (gunicorn, flask, python app.py...).
    atexit.register(_limpiar)
    return archivo.name


class Config:
    """Configuración base de la aplicación Flask."""

    # --- Entorno de ejecución ---
    # Producción si FLASK_ENV/APP_ENV=production, o variables de Render/Railway.
    FLASK_ENV = os.getenv('FLASK_ENV') or os.getenv('APP_ENV') or 'development'
    ES_PRODUCCION = (
        FLASK_ENV == 'production'
        or os.getenv('RENDER') == 'true'
        or bool(os.getenv('RAILWAY_RUNTIME'))
    )

    # --- Seguridad ---
    # SESSION_COOKIE_SAMESITE='Lax' mitiga CSRF; HTTPONLY=true mitiga XSS;
    # SECURE=true en producción (HTTPS). WTF_CSRF_TIME_LIMIT=None para que
    # el token no venza con la sesión (la cookie ya expira con la sesión).
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = ES_PRODUCCION

    # Flask-WTF CSRF: token sin límite de tiempo (None) para pestañas abiertas.
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']

    # SECRET_KEY: en producción DEBE estar en .env; en desarrollo usa una temporal.
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        if ES_PRODUCCION:
            raise ValueError(
                "SECRET_KEY no está definida en el .env y el entorno es "
                "producción. Agregá SECRET_KEY=<valor_largo_aleatorio> al "
                ".env (puede generarse con: python -c "
                "'import secrets; print(secrets.token_hex(32))'). "
                "Sin ella, las sesiones se invalidan en cada reinicio."
            )
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        # Sin emojis ni tildes raras que rompan consolas legacy (cp1252).
        print("\n[config] ADVERTENCIA: SECRET_KEY no definida en .env. "
              "Se usó una clave temporal en memoria. "
              "Esto es SOLO para desarrollo: las sesiones se invalidan en "
              "cada reinicio. En producción el arranque fallará hasta que "
              "definas SECRET_KEY en el .env.\n")

    # --- Base de datos (MySQL) ---
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'futuro360')
    DB_PORT = os.getenv('DB_PORT', '3306')
    # DB_SSL_CA: certificado CA para TLS/SSL (Aiven).
    #   1) DB_SSL_CA_CONTENT → contenido PEM (se escribe a archivo temporal).
    #   2) DB_SSL_CA → ruta al archivo PEM local.
    # Sin ninguna se conecta sin SSL.
    DB_SSL_CA = None
    _db_ssl_ca_content = os.getenv('DB_SSL_CA_CONTENT')
    if _db_ssl_ca_content:
        _archivo_ca = _materializar_ca(_db_ssl_ca_content)
        DB_SSL_CA = _archivo_ca
    else:
        _db_ssl_ca = os.getenv('DB_SSL_CA')
        if _db_ssl_ca:
            _ruta_ca = Path(_db_ssl_ca)
            if not _ruta_ca.is_absolute():
                _ruta_ca = Path(__file__).resolve().parent / _ruta_ca
            DB_SSL_CA = str(_ruta_ca)

    # --- Cuenta del panel (dueño del sistema) ---
    # La cuenta se crea automáticamente al iniciar (ver core/migraciones.py).
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'fabriciovillagra05@gmail.com')
    # Contraseña solo para la primera vez; después se cambia por recuperación.
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    if not ADMIN_PASSWORD:
        raise ValueError(
            "ADMIN_PASSWORD no está definida en el .env. "
            "Agregá ADMIN_PASSWORD=TuContraseña en el archivo .env antes de iniciar."
        )

    # --- URL pública del sitio ---
    URL_PUBLICA = os.getenv('RENDER_EXTERNAL_URL') or 'https://futuro-360.onrender.com'

    # --- Email (Resend) ----------------------------------------------------
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    MAIL_FROM = os.getenv('MAIL_FROM', 'Futuro 360 <onboarding@resend.dev>')

    # --- Brevo (recuperación de contraseña) ---
    # PIN vía API HTTPS (Render bloquea SMTP). SENDER_EMAIL debe estar
    # verificada en Brevo.
    BREVO_API_KEY = os.getenv('BREVO_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')

    # --- Cloudinary (imágenes y videos) ---
    # Si las 3 claves están definidas, sube a Cloudinary; si no, fallback local.
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME') or None
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY') or None
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET') or None


# --- Constantes de dominio ------------------------------------------------

# Extensiones de imagen aceptadas en las subidas de archivos (carreras y noticias).
EXTENSIONES_IMAGEN = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Extensiones de video aceptadas en las subidas (carreras y noticias).
EXTENSIONES_VIDEO = {'mp4', 'webm', 'mov', 'avi', 'mkv', 'm4v'}
