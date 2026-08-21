"""
Servicio de envío de correos electrónicos.

Centraliza TODO el envío de emails del sistema:
- ``enviar_mensaje_soporte``      → notificación de soporte al dueño (Resend).
- ``solicitar_pin``               → PIN de recuperación de contraseña (Brevo).
- ``notificar_cuenta_eliminada``  → aviso cuando se elimina una cuenta (Brevo).

El soporte va por Resend: llega únicamente al ADMIN_EMAIL, así que el modo
testing de Resend no lo afecta. El PIN va por la API HTTPS de Brevo porque
Render bloquea el SMTP saliente (puertos 25/465/587) en todos sus planes;
la API llega a CUALQUIER usuario y solo exige verificar la dirección
remitente en Brevo (sin comprar dominio).
(Historia: esto antes vivía en un servicio Node separado; ver
recuperacion/README.md.)
"""

import secrets

import requests
import resend
from markupsafe import escape

from config import Config

# Se configura la API key al importar el módulo.
# Es segura: si RESEND_API_KEY no está definida, el envío fallará con un
# mensaje claro en pantalla (el flujo lo maneja con try/except).
resend.api_key = Config.RESEND_API_KEY

# Validez del PIN de recuperación (en minutos). Única fuente de verdad: la
# usan el texto del correo (_html_pin) y los INSERT de password_resets en
# los blueprints de auth (sitio y admin), de modo que no pueden desincronizarse.
PIN_EXPIRA_MINUTOS = 15

# Endpoint y timeout (segundos) de la API de Brevo que envía los PIN.
# Si Brevo no responde en ese lapso se lanza un timeout y el caller muestra
# "No se pudo enviar el correo" en vez de colgar el request del usuario.
BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'
BREVO_TIMEOUT = 15


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


def _html_cuenta_eliminada(nombre: str, es_admin: bool) -> str:
    """
    Plantilla HTML del aviso de cuenta eliminada.

    Mismo criterio que _html_pin: CSS inline, tablas anidadas y paleta de
    Futuro 360 para máxima compatibilidad con los clientes de correo.
    El texto cambia según el rol de la cuenta eliminada:
    - admin   → indica que fue eliminada "por medidas de seguridad".
    - usuario → lo invita a volver a registrarse (botón a /registro).
    """
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
    """
    Envía un correo HTML por la API de Brevo (transporte común del sistema).

    - El remitente visible es "Futuro 360 <SENDER_EMAIL>" (verificado en Brevo).
    - Lanza RuntimeError con mensajes que distinguen el tipo de fallo
      (configuración faltante / rechazo de la API / timeout / conexión)
      para diagnosticar rápido en los logs. Ningún mensaje incluye la API key.
    """
    if not Config.BREVO_API_KEY or not Config.SENDER_EMAIL:
        raise RuntimeError(
            'BREVO_API_KEY / SENDER_EMAIL no están definidas en el '
            'entorno (.env local o variables de Render).')

    try:
        # La llamada es un POST HTTPS común (puerto 443, siempre permitido
        # en Render). El timeout aplica a conexión + respuesta: si Brevo no
        # contesta, explota a los ~15 s como máximo y nunca cuelga el request.
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

    # Brevo responde 201 Created cuando acepta el mensaje; cualquier otra
    # cosa (401 key inválida, 400 remitente no verificado, etc.) es un fallo.
    if respuesta.status_code >= 400:
        raise RuntimeError(
            f'Brevo rechazo el envio (HTTP {respuesta.status_code}): '
            f'{respuesta.text[:200]}')


def solicitar_pin(email: str) -> str:
    """
    Genera un PIN de 6 dígitos y lo envía por la API de Brevo a `email`.

    - Generación con `secrets` (CSPRNG).
    - Envío por HTTPS a api.brevo.com (puerto 443): Render bloquea el SMTP
      saliente, así que el correo viaja por la API. El remitente debe estar
      verificado en Brevo (SENDER_EMAIL); no hace falta dominio propio.
    - Devuelve el PIN (str) para que el blueprint lo guarde HASHEADO en
      password_resets con generate_password_hash.
    - Lanza RuntimeError (ver _enviar_por_brevo) si el envío falla.
    """
    pin = str(secrets.randbelow(900000) + 100000)  # 100000..999999
    _enviar_por_brevo(email, 'Recuperación de contraseña', _html_pin(pin))
    return pin


def notificar_cuenta_eliminada(email: str, nombre: str, es_admin: bool) -> None:
    """
    Avisa a `email` que su cuenta fue eliminada del sistema.

    - es_admin=True  → el texto indica que fue eliminada "por medidas de
      seguridad" (caso de cuentas de administrador borradas desde el panel).
    - es_admin=False → invita a volver a registrarse con enlace a /registro
      (caso de usuarios comunes, tanto por panel como por auto-baja).
    - Lanza RuntimeError si el envío falla (ver _enviar_por_brevo): quien
      llama decide si el fallo afecta al flujo o solo se registra en logs.
    """
    _enviar_por_brevo(
        email,
        'Tu cuenta fue eliminada - Futuro 360',
        _html_cuenta_eliminada(nombre, es_admin),
    )


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
