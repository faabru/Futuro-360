"""
Paquete `blueprints`: módulos de rutas de la aplicación.

La aplicación se organiza en dos grandes grupos de rutas:

- ``blueprints.sitio``  → sitio público (auth, principal, vocacional, carreras,
                          juegos, noticias).
- ``blueprints.admin``  → panel de administración (auth, dashboard, usuarios,
                          orientaciones, carreras, preguntas, juego, noticias,
                          reportes).

``registrar_blueprints(app)`` se encarga de registrar todos los blueprints en
la aplicación creada por ``create_app``.
"""


def registrar_blueprints(app):
    """Registra todos los blueprints del sitio público y del panel admin."""
    from blueprints.sitio.auth import bp as sitio_auth_bp
    from blueprints.sitio.principal import bp as sitio_principal_bp
    from blueprints.sitio.vocacional import bp as sitio_vocacional_bp
    from blueprints.sitio.carreras import bp as sitio_carreras_bp
    from blueprints.sitio.juegos import bp as sitio_juegos_bp
    from blueprints.sitio.noticias import bp as sitio_noticias_bp
    from blueprints.sitio.legal import bp as sitio_legal_bp

    from blueprints.admin.auth import bp as admin_auth_bp
    from blueprints.admin.dashboard import bp as admin_dashboard_bp
    from blueprints.admin.usuarios import bp as admin_usuarios_bp
    from blueprints.admin.orientaciones import bp as admin_orientaciones_bp
    from blueprints.admin.carreras import bp as admin_carreras_bp
    from blueprints.admin.preguntas import bp as admin_preguntas_bp
    from blueprints.admin.juego import bp as admin_juego_bp
    from blueprints.admin.noticias import bp as admin_noticias_bp
    from blueprints.admin.reportes import bp as admin_reportes_bp

    for bp in [sitio_auth_bp, sitio_principal_bp, sitio_vocacional_bp,
               sitio_carreras_bp, sitio_juegos_bp, sitio_noticias_bp,
               sitio_legal_bp,
               admin_auth_bp, admin_dashboard_bp, admin_usuarios_bp,
               admin_orientaciones_bp, admin_carreras_bp, admin_preguntas_bp,
               admin_juego_bp, admin_noticias_bp, admin_reportes_bp]:
        app.register_blueprint(bp)
