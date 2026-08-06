"""
Servicio de envío de correos electrónicos (Resend).

Centraliza el envío de emails para que ningún blueprint tenga que conocer la
API de Resend. Se usa para la recuperación de contraseña del sitio público y
del panel de administración.
"""

import random

import resend

from config import Config

# Se configura la API key al importar el módulo.
# Es segura: si RESEND_API_KEY no está definida, el envío fallará con un
# mensaje claro en pantalla (el flujo de recuperación lo maneja con try/except).
resend.api_key = Config.RESEND_API_KEY


def _plantilla_correo(codigo: str, panel: bool) -> str:
    """Devuelve el HTML del correo según sea para el sitio (panel=False)
    o para el panel de administración (panel=True)."""
    color = '#dc3545' if panel else '#0d6efd'
    titulo_sistema = 'Panel Admin - Futuro 360' if panel else 'Futuro 360'
    return f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;">
        <div style="background-color: {color}; padding: 20px; text-align: center; color: white;">
            <h1 style="margin: 0;">{'🛡️' if panel else '🎓'} {titulo_sistema}</h1>
        </div>
        <div style="padding: 30px; line-height: 1.6; color: #333;">
            <h2 style="color: {color}; text-align: center;">Recuperación de contraseña</h2>
            <p style="text-align: center;">Ingresá este código en {'el panel' if panel else 'la plataforma'} para continuar:</p>
            <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: {color};">{codigo}</span>
            </div>
            <p style="text-align: center; font-size: 0.9em; color: #666;">⏱️ Este código expira en 15 minutos.</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="text-align: center; font-size: 0.8em; color: #999;">Si no solicitaste este cambio, ignorá este mensaje.</p>
        </div>
        <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 0.75em; color: #999;">
            Futuro 360 · Orientación Vocacional · Tucumán, Argentina
        </div>
    </div>
    """


def generar_codigo() -> str:
    """Genera un código PIN de 6 dígitos para la recuperación de contraseña."""
    return str(random.randint(100000, 999999))


def enviar_codigo_reset(destinatario: str, codigo: str, panel: bool = False) -> None:
    """
    Envía un correo con el código de verificación.

    Parámetros:
    - destinatario: dirección de correo del usuario.
    - codigo: PIN de 6 dígitos generado con ``generar_codigo``.
    - panel: True si el correo corresponde al panel de administración.

    Lanza una excepción si el envío falla (quien llama la maneja para mostrar
    un mensaje de error al usuario).
    """
    asunto = (
        '🔐 Tu código de verificación - Panel Admin Futuro 360'
        if panel else
        '🔐 Tu código de verificación - Futuro 360'
    )
    resend.Emails.send({
        "from": Config.MAIL_FROM,
        "to": [destinatario],
        "subject": asunto,
        "html": _plantilla_correo(codigo, panel),
    })
