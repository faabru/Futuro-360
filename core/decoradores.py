"""
Decoradores de autorización y control de acceso.

Concentran toda la lógica de permisos del sistema, que puede resumirse en:

1. ``requiere_login``  → exige una sesión de usuario del sitio público.
2. ``requiere_admin``  → exige sesión del panel O un usuario con rol admin.
3. ``ajax_o_redirect`` → si la petición es AJAX responde JSON; si no, ejecuta
                         la vista normalmente (permite reutilizar un POST
                         tanto desde fetch() como desde un formulario común).
4. ``es_usuario_dueño``→ indica si el usuario logueado es el dueño del panel.

Los decoradores NO dependen de ningún blueprint en particular: redirigen a
endpoints de navegación (login / dashboard) que están definidos en los
blueprints del sitio.
"""

from functools import wraps

from flask import (flash, g, get_flashed_messages, jsonify, redirect, request,
                   session, url_for)

# Nombre de los endpoints de destino (están en el blueprint `auth` y `principal`).
ENDPOINT_LOGIN = 'auth.login'
ENDPOINT_DASHBOARD = 'principal.dashboard'


def es_ajax():
    """
    True si la petición fue hecha con fetch()/AJAX.

    El frontend envía la cabecera ``X-Requested-With: XMLHttpRequest`` en
    todas sus llamadas fetch().
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def ajax_o_redirect(f):
    """
    Decorador que permite responder a un POST tanto por AJAX como por
    formulario tradicional sin duplicar código.

    - Si la petición es AJAX: limpia los flash acumulados y responde
      ``{"ok": true}`` (el JS actualiza la interfaz sin recargar).
    - Si no: ejecuta la vista normal (que hace redirect con su mensaje flash).
    """
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
    """
    Exige que el usuario haya iniciado sesión en el sitio público.

    Si no hay sesión, guarda un mensaje y redirige a la pantalla de login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for(ENDPOINT_LOGIN))
        return f(*args, **kwargs)
    return decorated_function


def requiere_admin(f):
    """
    Exige privilegios de administración.

    Se considera autorizado si:
    - Ya tiene una sesión del panel activa (``session['admin_autenticado']``), o
    - Está logueado en el sitio con rol ``admin``.

    Cualquier otro caso redirige a login (sin sesión) o al dashboard (usuario
    común sin permisos).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Acceso directo: sesión exclusiva del panel (botón "Panel Admin").
        if session.get('admin_autenticado'):
            return f(*args, **kwargs)
        if g.user is None:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for(ENDPOINT_LOGIN))
        if g.user.get('rol') != 'admin':
            flash('No tienes permisos para acceder a esta sección.', 'danger')
            return redirect(url_for(ENDPOINT_DASHBOARD))
        return f(*args, **kwargs)
    return decorated_function


def es_usuario_dueño():
    """
    Indica si la persona logueada es el dueño del panel.

    Puede determinarse de dos maneras:
    - Desde la sesión del panel (``admin_es_dueño``), o
    - Desde el login normal del sitio (campo ``es_dueño`` de la tabla usuarios).

    El dueño tiene permisos exclusivos: editar/eliminar a otros administradores.
    """
    if session.get('admin_es_dueño'):
        return True
    if g.user is not None and g.user.get('es_dueño'):
        return True
    return False
