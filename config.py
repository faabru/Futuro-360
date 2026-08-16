"""
Configuración central de Futuro 360.

Este módulo concentra TODA la configuración de la aplicación en un solo lugar:
credenciales, variables de entorno, constantes de dominio y opciones de Flask.

De esta manera, un nuevo desarrollador sabe dónde mirar para ajustar el
comportamiento del sistema sin tener que recorrer el código buscando valores
"hardcodeados".
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

    Útil para plataformas (Render/Railway) donde el certificado llega por la
    variable ``DB_SSL_CA_CONTENT`` y no puede subirse al repositorio.

    - Valida que el PEM contenga ``BEGIN CERTIFICATE`` y ``END CERTIFICATE``.
    - Conserva los saltos de línea tal como vienen (normaliza a LF) para que
      el archivo sea un PEM válido.
    - Usa ``tempfile.NamedTemporaryFile`` en el directorio temporal del SISTEMA
      (nunca dentro del proyecto), con permisos restrictivos.
    - Registra el borrado seguro del archivo con ``atexit`` para que se elimine
      cuando el proceso termine.

    Devuelve la ruta (str) del archivo temporal, o ``None`` si el contenido no
    es un PEM válido (en cuyo caso se conecta sin SSL y se informa en consola).
    """
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

    # --- Seguridad -------------------------------------------------------
    # Clave usada por Flask para firmar las cookies de sesión. En producción
    # DEBE definirse en el archivo .env con un valor largo y aleatorio.
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        print("[config] SECRET_KEY no definida en .env — usando clave temporal. "
              "Las sesiones no persistirán entre reinicios.")

    # --- Base de datos (MySQL) -------------------------------------------
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'futuro360')
    # Puerto de MySQL (Aiven usa uno propio). Default 3306 si no está definido.
    DB_PORT = os.getenv('DB_PORT', '3306')
    # Certificado CA para conexión TLS/SSL (Aiven). Se resuelve de una de dos
    # formas según el entorno:
    #
    #   1) DB_SSL_CA_CONTENT  → el contenido del certificado PEM. Pensado para
    #      plataformas como Render/Railway donde el certificado no se sube al
    #      repositorio: se define esta variable con el texto completo del PEM y
    #      la app lo escribe a un archivo temporal del SISTEMA (nunca dentro
    #      del proyecto) para que mysql-connector-python (que requiere una
    #      ruta física) lo use.
    #
    #   2) DB_SSL_CA  → ruta al archivo PEM local (desarrollo). Se resuelve a
    #      una ruta absoluta relativa a la raíz del proyecto para que funcione
    #      sin importar desde qué directorio se ejecute Flask.
    #
    # Si no se define ninguna, la conexión sigue usando el comportamiento local
    # sin SSL. Nunca se desactiva la verificación del certificado.
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

    # --- Cuenta del panel (dueño del sistema) -----------------------------
    # El acceso al panel es solo por email. La cuenta con este correo se crea
    # automáticamente al iniciar (ver core/migraciones.py) con rol admin y la
    # marca es_dueño, que le otorga permisos exclusivos sobre otros admins.
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'fabriciovillagra05@gmail.com')
    # Contraseña SOLO usada la primera vez que se crea la cuenta del dueño
    # (su propio .env, aparte del de tu compañera). Una vez creada, se puede
    # cambiar desde el flujo de recuperación.
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    if not ADMIN_PASSWORD:
        raise ValueError(
            "ADMIN_PASSWORD no está definida en el .env. "
            "Agregá ADMIN_PASSWORD=TuContraseña en el archivo .env antes de iniciar."
        )

    # --- Email (Resend) ----------------------------------------------------
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    MAIL_FROM = os.getenv('MAIL_FROM', 'Futuro 360 <onboarding@resend.dev>')

    # --- Cloudinary (imágenes y videos) --------------------------------------
    # Si las tres claves están definidas, las subidas van a Cloudinary y se
    # guardan como URL (compartida entre máquinas). Sin claves, se sigue
    # guardando en static/imagenes/ (fallback local).
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME') or None
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY') or None
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET') or None


# --- Constantes de dominio ------------------------------------------------

# Extensiones de imagen aceptadas en las subidas de archivos (carreras y noticias).
EXTENSIONES_IMAGEN = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Extensiones de video aceptadas en las subidas (carreras y noticias).
EXTENSIONES_VIDEO = {'mp4', 'webm', 'mov', 'avi', 'mkv', 'm4v'}
