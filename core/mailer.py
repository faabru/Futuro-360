"""
Servicio de envío de correos electrónicos.
PIN de recuperación y aviso de cuenta eliminada → Brevo API.
Soporte/consulta → Resend.
"""

import secrets

import requests
import resend
from markupsafe import escape

from config import Config

# API key de Resend al importar el módulo.
resend.api_key = Config.RESEND_API_KEY

# Validez del PIN (fuente de verdad compartida por mailer + auth).
PIN_EXPIRA_MINUTOS = 15

# Endpoint y timeout de Brevo.
BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'
BREVO_TIMEOUT = 15


def _html_pin(pin: str) -> str:
    """Plantilla HTML del correo del PIN (CSS inline, tablas anidadas para Outlook)."""
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


def _html_cuenta_eliminada(nombre: str, es_admin: bool) -> str:
    """Plantilla del aviso de cuenta eliminada. Texto según rol (admin/usuario)."""
    # El nombre lo escribió el propio usuario al registrarse: se escapa para
    # que no pueda inyectar HTML dentro del correo.
    nombre_seguro = escape(nombre)

    if es_admin:
        parrafo = ('Tu cuenta de <strong>administrador</strong> fue eliminada '
                   'del sistema por <strong>medidas de seguridad</strong>.')
        extra = ('<p style="margin:22px 0 0 0; font-size:14px; line-height:1.6; color:#2A7390;">'
                 '&#128274; Si cre&eacute;s que esto fue un error, contactate con el equipo '
                 'de Futuro 360 desde el centro de soporte de la plataforma.</p>')
    else:
        parrafo = ('Tu cuenta fue eliminada de <strong>Futuro 360</strong>. '
                   'Si quer&eacute;s seguir explorando la orientaci&oacute;n vocacional, '
                   'pod&eacute;s registrarte nuevamente cuando quieras.')
        enlace = f'{Config.URL_PUBLICA}/registro'
        extra = ('<table role="presentation" cellpadding="0" cellspacing="0" align="center" '
                 'style="margin:26px auto 0 auto;">'
                 '<tr><td style="background-color:#2F8EAB; border-radius:10px;">'
                 f'<a href="{enlace}" style="display:inline-block; padding:13px 34px; '
                 'font-family:Arial,Helvetica,sans-serif; font-size:15px; font-weight:bold; '
                 'color:#FFFFFF; text-decoration:none;">Volver a registrarme</a>'
                 '</td></tr></table>')

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
                        <h1 style="margin:0 0 8px 0; font-size:21px; font-weight:bold; color:#142B38;">Tu cuenta fue eliminada</h1>
                        <p style="margin:0 0 18px 0; font-size:14px; line-height:1.6; color:#2A7390;">Hola {nombre_seguro}:</p>
                        <p style="margin:0; font-size:14px; line-height:1.6; color:#142B38;">{parrafo}</p>
                        {extra}
                        <hr style="border:none; border-top:1px solid #C6E2EC; margin:26px 0;">
                        <p style="margin:0; font-size:13px; line-height:1.6; color:#2A7390;">Este es un aviso autom&aacute;tico del sistema. Si no esperabas este correo, pod&eacute;s ignorarlo.</p>
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


def _enviar_por_brevo(destinatario: str, asunto: str, html: str) -> None:
    """Envía correo HTML por la API de Brevo (HTTPS, puerto 443).
    Lanza RuntimeError si falla (configuración, API, timeout, conexión)."""
    if not Config.BREVO_API_KEY or not Config.SENDER_EMAIL:
        raise RuntimeError(
            'BREVO_API_KEY / SENDER_EMAIL no están definidas en el '
            'entorno (.env local o variables de Render).')

    try:
        # POST HTTPS a api.brevo.com (siempre permitido en Render).
        respuesta = requests.post(
            BREVO_API_URL,
            headers={
                'api-key': Config.BREVO_API_KEY,
                'accept': 'application/json',
                'content-type': 'application/json',
            },
            json={
                # Nombre visible personalizado; la dirección debe coincidir
                # con un remitente verificado en la cuenta de Brevo.
                'sender': {'name': 'Futuro 360', 'email': Config.SENDER_EMAIL},
                'to': [{'email': destinatario}],
                'subject': asunto,
                'htmlContent': html,
            },
            timeout=BREVO_TIMEOUT,
        )
    except requests.exceptions.Timeout as e:
        raise RuntimeError(
            f'Timeout ({BREVO_TIMEOUT}s): la API de Brevo no respondio '
            '(problema de red o de Brevo).') from e
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f'No se pudo conectar a api.brevo.com: {e}') from e

    # Brevo responde 201 Created; cualquier otro código es fallo.
    if respuesta.status_code >= 400:
        raise RuntimeError(
            f'Brevo rechazo el envio (HTTP {respuesta.status_code}): '
            f'{respuesta.text[:200]}')


def solicitar_pin(email: str) -> str:
    """Genera PIN de 6 dígitos, lo envía por Brevo y lo devuelve (str).
    El blueprint lo guarda hasheado en password_resets."""
    pin = str(secrets.randbelow(900000) + 100000)  # 100000..999999
    _enviar_por_brevo(email, 'Recuperación de contraseña', _html_pin(pin))
    return pin


def notificar_cuenta_eliminada(email: str, nombre: str, es_admin: bool) -> None:
    """Avisa por correo que la cuenta fue eliminada. Texto según rol."""
    _enviar_por_brevo(
        email,
        'Tu cuenta fue eliminada - Futuro 360',
        _html_cuenta_eliminada(nombre, es_admin),
    )


def enviar_mensaje_soporte(nombre: str, email: str, asunto: str, mensaje: str) -> None:
    """Envía al dueño (ADMIN_EMAIL) un correo de notificación de soporte."""
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
