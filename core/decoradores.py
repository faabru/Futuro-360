"""
Decoradores de autorización y control de acceso.

Concentran toda la lógica de permisos del sistema, que puede resumirse en:

1. ``requiere_login``  → exige una sesión de usuario del sitio público.
2. ``requiere_admin``  → exige la sesión exclusiva del panel (independiente
                         del login del sitio: aunque la persona tenga rol admin
                         en la web, debe autenticarse por separado).
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
    Exige una sesión activa del panel de administración.

    El acceso al panel es independiente de la sesión del sitio público: aunque
    la persona esté logueada en la web con rol admin, debe autenticarse por
    separado en ``/admin/login`` con su email y contraseña de administrador.
    Cualquier otro caso redirige al login del panel.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('admin_autenticado'):
            return f(*args, **kwargs)
        flash('Debés iniciar sesión como administrador para acceder al panel.', 'warning')
        return redirect(url_for('admin_auth.admin_login'))
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
