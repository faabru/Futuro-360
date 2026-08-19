"""
Servicio de envío de correos electrónicos (Resend).

Centraliza el envío de emails de notificación de soporte. La recuperación de
contraseña NO se envía desde acá: la maneja el servidor Node del prototipo
("recuperacion de contraseña/server.js"), que genera el PIN y lo manda por
Resend. El flujo Python solo le pide el PIN (ver blueprints de auth).
"""

import resend

from config import Config

# Se configura la API key al importar el módulo.
# Es segura: si RESEND_API_KEY no está definida, el envío fallará con un
# mensaje claro en pantalla (el flujo lo maneja con try/except).
resend.api_key = Config.RESEND_API_KEY


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
