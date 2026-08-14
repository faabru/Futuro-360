"""
Configuración central de Futuro 360.

Este módulo concentra TODA la configuración de la aplicación en un solo lugar:
credenciales, variables de entorno, constantes de dominio y opciones de Flask.

De esta manera, un nuevo desarrollador sabe dónde mirar para ajustar el
comportamiento del sistema sin tener que recorrer el código buscando valores
"hardcodeados".
"""

import os

from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (BD, secretos, emails, etc.).
# Si el archivo no existe, se usan los valores por defecto definidos abajo.
load_dotenv()


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
