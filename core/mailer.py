"""
Servicio de envío de correos electrónicos.

Centraliza TODO el envío de emails del sistema:
- ``enviar_mensaje_soporte`` → notificación de soporte al dueño (Resend).
- ``solicitar_pin``          → PIN de recuperación de contraseña (Gmail SMTP).

El soporte va por Resend: llega únicamente al ADMIN_EMAIL, así que el modo
testing de Resend no lo afecta. El PIN va por Gmail SMTP para poder llegar
a CUALQUIER usuario sin depender de verificar un dominio externo.
(Historia: esto antes vivía en un prototipo Node; ver
docs/prototipo-node-recuperacion/README.md.)
"""

import secrets
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# Timeout (segundos) para conectar/autenticar/enviar contra smtp.gmail.com.
# Si Gmail no responde en ese lapso se lanza un timeout y el caller muestra
# "No se pudo enviar el correo" en vez de colgar el request del usuario.
GMAIL_SMTP_TIMEOUT = 15


def _html_pin(pin: str) -> str:
    """
    Plantilla HTML del correo del PIN.

    Todo el CSS va INLINE (style="...") porque Gmail, Outlook y otros
    clientes recortan las etiquetas <style> del head. El layout usa tablas
    anidadas: es lo unico que Outlook renderiza de forma confiable.
    Paleta: identidad de Futuro 360 (static/style.css :root).
    Los acentos y emojis van como entidades HTML para maxima compatibilidad.
    """
    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#EAF4F9;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#EAF4F9;">
    <tr>
        <td align="center" style="padding:32px 12px;">
            <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%; max-width:600px; background-color:#ffffff; border:1px solid #C6E2EC; border-radius:16px; overflow:hidden;">
                <tr>
                    <td style="background-color:#142B38; padding:30px 40px; text-align:center;">
                        <div style="font-family:Arial,Helvetica,sans-serif; font-size:22px; font-weight:bold; color:#FFFFFF;">&#127891; Futuro 360</div>
                        <div style="font-family:Arial,Helvetica,sans-serif; font-size:13px; color:#B7E0EA; margin-top:4px;">Orientaci&oacute;n Vocacional</div>
                    </td>
                </tr>
                <tr>
                    <td style="padding:36px 40px; font-family:Arial,Helvetica,sans-serif; color:#142B38;">
                        <h1 style="margin:0 0 8px 0; font-size:21px; font-weight:bold; color:#142B38;">Tu PIN es:</h1>
                        <p style="margin:0 0 24px 0; font-size:14px; line-height:1.6; color:#2A7390;">Ingres&aacute; este c&oacute;digo de 6 d&iacute;gitos en la p&aacute;gina de verificaci&oacute;n para continuar con la recuperaci&oacute;n de tu contrase&ntilde;a.</p>
                        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="background-color:#EAF4F9; border:1px solid #C6E2EC; border-radius:12px; padding:22px 16px;">
                                    <span style="font-family:Arial,Helvetica,sans-serif; font-size:42px; font-weight:bold; letter-spacing:12px; color:#2F8EAB;">{pin}</span>
                                </td>
                            </tr>
                        </table>
                        <p style="margin:22px 0 0 0; font-size:14px; color:#142B38;">&#9201; El c&oacute;digo vence en <strong>{PIN_EXPIRA_MINUTOS} minutos</strong>.</p>
                        <hr style="border:none; border-top:1px solid #C6E2EC; margin:26px 0;">
                        <p style="margin:0; font-size:13px; line-height:1.6; color:#2A7390;">&#128274; Si no solicitaste este c&oacute;digo, pod&eacute;s ignorar este correo. Tu contrase&ntilde;a actual no fue modificada.</p>
                    </td>
                </tr>
                <tr>
                    <td style="background-color:#EAF4F9; padding:16px 40px; text-align:center; font-family:Arial,Helvetica,sans-serif; font-size:12px; color:#2A7390;">
                        Futuro 360 &middot; Orientaci&oacute;n Vocacional &middot; Tucum&aacute;n, Argentina
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
</html>"""


def solicitar_pin(email: str) -> str:
    """
    Genera un PIN de 6 dígitos y lo envía por Gmail SMTP a `email`.

    - Generación con `secrets` (CSPRNG).
    - Envío por SMTP_SSL al puerto 465 (TLS implícito desde el primer byte).
    - Autenticación con la contraseña de APLICACIÓN (GMAIL_APP_PASSWORD),
      nunca con la contraseña normal de la cuenta.
    - Devuelve el PIN (str) para que el blueprint lo guarde HASHEADO en
      password_resets con generate_password_hash.
    - Lanza RuntimeError con un mensaje que distingue el tipo de fallo
      (credenciales / timeout / conexión) para que sea rápido de diagnosticar
      en los logs. Ningún mensaje incluye la contraseña de aplicación.
    """
    if not Config.GMAIL_USER or not Config.GMAIL_APP_PASSWORD:
        raise RuntimeError(
            'GMAIL_USER / GMAIL_APP_PASSWORD no están definidas en el '
            'entorno (.env local o variables de Render).')

    pin = str(secrets.randbelow(900000) + 100000)  # 100000..999999

    # Arma el mensaje MIME: cabeceras + cuerpo HTML (utf-8 maneja los acentos).
    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = 'Recuperación de contraseña'
    # Nombre visible personalizado; la dirección real es la cuenta autenticada.
    mensaje['From'] = f'Futuro 360 <{Config.GMAIL_USER}>'
    mensaje['To'] = email
    mensaje.attach(MIMEText(_html_pin(pin), 'html', 'utf-8'))

    try:
        # SMTP_SSL (465): el canal ya nace cifrado, sin negociación STARTTLS.
        # El timeout aplica a conexión + login + envío: si Gmail no responde,
        # explota a los ~15 s como máximo y nunca cuelga el request.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465,
                              timeout=GMAIL_SMTP_TIMEOUT) as smtp:
            smtp.login(Config.GMAIL_USER, Config.GMAIL_APP_PASSWORD)
            smtp.send_message(mensaje)
    except smtplib.SMTPAuthenticationError as e:
        # Credenciales inválidas: app password mal copiado, revocado, o 2FA
        # desactivada. La respuesta de Gmail NO incluye la contraseña.
        raise RuntimeError(
            'Gmail rechazo las credenciales SMTP (revisa GMAIL_USER y '
            f'GMAIL_APP_PASSWORD): {e}') from e
    except (socket.timeout, TimeoutError) as e:
        raise RuntimeError(
            f'Timeout ({GMAIL_SMTP_TIMEOUT}s): smtp.gmail.com no respondio '
            '(problema de red o de Gmail).') from e
    except OSError as e:
        # Resto de errores de red: DNS, conexion rechazada, reset, etc.
        raise RuntimeError(
            f'No se pudo conectar a smtp.gmail.com: {e}') from e

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
