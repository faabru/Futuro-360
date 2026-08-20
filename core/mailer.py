"""
Servicio de envío de correos electrónicos (Resend).

Centraliza TODO el envío de emails del sistema:
- ``enviar_mensaje_soporte`` → notificación de soporte al dueño.
- ``solicitar_pin``          → PIN de recuperación de contraseña.

La recuperación vivía en un prototipo Node separado; desde la migración
(ver docs/prototipo-node-recuperacion/README.md) el PIN se genera acá con
``secrets`` (CSPRNG) y se envía directo por Resend: nunca viaja por HTTP
entre servicios y no depende de un segundo proceso activo.
"""

import secrets

import resend

from config import Config

# Se configura la API key al importar el módulo.
# Es segura: si RESEND_API_KEY no está definida, el envío fallará con un
# mensaje claro en pantalla (el flujo lo maneja con try/except).
resend.api_key = Config.RESEND_API_KEY

# Validez del PIN de recuperación (en minutos). Única fuente de verdad: la
# usan el texto del correo (_html_pin) y los INSERT de password_resets en
# los blueprints de auth (sitio y admin), de modo que no pueden desincronizarse.
PIN_EXPIRA_MINUTOS = 15


def _html_pin(pin: str) -> str:
    """Plantilla HTML del correo del PIN (misma que usaba el prototipo Node)."""
    return f"""
        <h1>Tu PIN es:</h1>
        <h2>{pin}</h2>
        <p>El código vence en {PIN_EXPIRA_MINUTOS} minutos.</p>
    """


def solicitar_pin(email: str) -> str:
    """
    Genera un PIN de 6 dígitos y lo envía por Resend a `email`.

    Reemplaza al prototipo Node ("docs/prototipo-node-recuperacion/"):
    - Generación con `secrets` (CSPRNG) en lugar de Math.random() del Node.
    - Devuelve el PIN (str) para que el blueprint lo guarde HASHEADO en
      password_resets con generate_password_hash, igual que antes.
    - Lanza excepción si el envío falla (el caller ya la maneja con try/except).
    """
    pin = str(secrets.randbelow(900000) + 100000)  # 100000..999999
    resend.Emails.send({
        "from": Config.MAIL_FROM,
        "to": [email],
        "subject": "Recuperación de contraseña",
        "html": _html_pin(pin),
    })
    return pin


def enviar_mensaje_soporte(nombre: str, email: str, asunto: str, mensaje: str) -> None:
    """
    Envía al dueño (ADMIN_EMAIL) un correo de notificación con el mensaje
    recibido desde el centro de soporte.

    Lanza una excepción si el envío falla (quien llama la decide manejar).
    """
    resend.Emails.send({
        "from": Config.MAIL_FROM,
        "to": [Config.ADMIN_EMAIL],
        "subject": f"📬 Mensaje de soporte - {asunto}",
        "html": f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;">
            <div style="background-color: #0d6efd; padding: 20px; text-align: center; color: white;">
                <h1 style="margin: 0;">🎓 Futuro 360 · Centro de Soporte</h1>
            </div>
            <div style="padding: 30px; line-height: 1.6; color: #333;">
                <h2 style="color: #0d6efd;">Nuevo mensaje de soporte</h2>
                <p><strong>Asunto:</strong> {asunto}</p>
                <p><strong>Nombre:</strong> {nombre}</p>
                <p><strong>Email:</strong> {email}</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 16px 0;">
                <p><strong>Mensaje:</strong></p>
                <div style="background-color: #f8f9fa; padding: 16px; border-radius: 6px; color: #333;">{mensaje}</div>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 0.75em; color: #999;">
                Futuro 360 · Orientación Vocacional · Tucumán, Argentina
            </div>
        </div>
        """,
    })
