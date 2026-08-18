"""
Rutas legales y de soporte del sitio público.

- ``soporte``  → centro de soporte y contacto (guarda mensajes en `comentarios`).
- ``terminos`` → términos y condiciones de uso.
- ``privacidad`` → política de privacidad.
"""

from flask import Blueprint, render_template, request

from core.mailer import enviar_mensaje_soporte
from database_handler import obtener_db

bp = Blueprint('legal', __name__)


@bp.route('/soporte', methods=['GET', 'POST'])
def soporte():
    """Página de soporte y contacto de Futuro 360."""
    enviado = False
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        mensaje = request.form.get('mensaje', '').strip()
        asunto = request.form.get('asunto', 'Consulta general')

        if nombre and email and mensaje:
            # Guardar el mensaje en la tabla comentarios (ya existe en la BD)
            db = obtener_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO comentarios (nombre, email, mensaje) VALUES (%s, %s, %s)",
                (f"[{asunto}] {nombre}", email, mensaje)
            )
            db.commit()
            # Notificar al dueño (ADMIN_EMAIL) por correo. Si el envío falla,
            # el mensaje igual quedó guardado en la BD.
            try:
                enviar_mensaje_soporte(nombre, email, asunto, mensaje)
            except Exception:
                pass
            enviado = True

    return render_template('sitio/soporte.html', enviado=enviado)


@bp.route('/terminos')
def terminos():
    """Términos y condiciones de uso de Futuro 360."""
    return render_template('sitio/terminos.html')


@bp.route('/privacidad')
def privacidad():
    """Política de privacidad de Futuro 360."""
    return render_template('sitio/privacidad.html')