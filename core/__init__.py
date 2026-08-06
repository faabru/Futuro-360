"""
Paquete `core`: componentes transversales de la aplicación.

Agrupa toda la lógica que NO es una ruta en sí misma pero que las rutas
necesitan: decoradores de autorización, envío de emails, migraciones de la
base de datos y tareas de inicio.

Estructura:
- decoradores.py  → control de acceso (login, admin, dueño, AJAX).
- mailer.py       → envío de correos con Resend.
- migraciones.py  → creación/actualización automática de tablas.
- startup.py      → tareas que se ejecutan al arrancar la aplicación.
"""
