"""
Decoradores de autorización: requiere_login, requiere_admin,
ajax_o_redirect, es_usuario_dueño.
"""

from functools import wraps

from flask import (flash, g, get_flashed_messages, jsonify, redirect, request,
                   session, url_for)

# Endpoints de destino (en blueprints auth y principal).
ENDPOINT_LOGIN = 'auth.login'
ENDPOINT_DASHBOARD = 'principal.dashboard'


def es_ajax():
    """True si la petición es fetch()/AJAX (cabecera X-Requested-With)."""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def ajax_o_redirect(f):
    """Permite responder POST por AJAX (JSON) o formulario (redirect)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resultado = f(*args, **kwargs)
        if es_ajax():
            # Descartar mensajes flash para no arrastrarlos al recargar la página.
            list(get_flashed_messages())
            return jsonify(ok=True)
        return resultado
    return decorated_function


def requiere_login(f):
    """Exige sesión del sitio público. Si no hay, redirige a /login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for(ENDPOINT_LOGIN))
        return f(*args, **kwargs)
    return decorated_function


def requiere_admin(f):
    """Exige sesión del panel admin (independiente del login del sitio)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('admin_autenticado'):
            return f(*args, **kwargs)
        flash('Debés iniciar sesión como administrador para acceder al panel.', 'warning')
        return redirect(url_for('admin_auth.admin_login'))
    return decorated_function


def es_usuario_dueño():
    """True si el logueado es el dueño del panel (sesión o campo es_dueño)."""
    if session.get('admin_es_dueño'):
        return True
    if g.user is not None and g.user.get('es_dueño'):
        return True
    return False
