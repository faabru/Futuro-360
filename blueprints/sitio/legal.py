"""
Rutas legales y de soporte: soporte/contacto, términos y privacidad.
"""

from flask import Blueprint, g, redirect, render_template, request, url_for

from core.mailer import enviar_mensaje_soporte
from database_handler import obtener_db

bp = Blueprint('legal', __name__)


@bp.route('/soporte', methods=['GET', 'POST'])
def soporte():
    """Página de soporte y contacto de Futuro 360.
    Si el usuario está logueado, redirige al dashboard."""
    if g.user:
        return redirect(url_for('principal.dashboard'))
    enviado = False
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        mensaje = request.form.get('mensaje', '').strip()
        asunto = request.form.get('asunto', 'Consulta general')

        if nombre and email and mensaje:
            # Guardar en BD.
            db = obtener_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO comentarios (nombre, email, mensaje) VALUES (%s, %s, %s)",
                (f"[{asunto}] {nombre}", email, mensaje)
            )
            db.commit()
            # Notificar al dueño. Si el envío falla, el mensaje queda guardado.
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