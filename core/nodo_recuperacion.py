"""
Cliente del servidor Node de recuperación de contraseña.

El prototipo Node ("recuperacion de contraseña/server.js") genera el PIN y
lo envía por Resend. Este módulo le pide el PIN a ese servidor y, si no está
activo, lo levanta automáticamente (subprocess) para que la recuperación
funcione sin pasos manuales.
"""

import subprocess
import sys
import time

import requests

from config import Config

RUTA_FOLDER_NODE = 'recuperacion de contraseña'


def _server_activo(url: str, timeout: float = 1.0) -> bool:
    """Devuelve True si el servidor Node responde en la URL dada."""
    try:
        requests.post(url, json={'email': 'health@check.com'}, timeout=timeout)
        return True
    except Exception:
        return False


def _iniciar_server(url: str) -> bool:
    """
    Intenta levantar el servidor Node en background desde la carpeta del
    prototipo. Devuelve True si quedó respondiendo (o ya lo estaba).
    """
    import os
    import shutil

    ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(ruta_proyecto, RUTA_FOLDER_NODE)
    server_js = os.path.join(folder, 'server.js')

    if not os.path.exists(server_js):
        return False

    node = shutil.which('node')
    if not node:
        return False

    # Sin ventana de consola en Windows (CREATION_NO_WINDOW = 0x08000000).
    flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
    try:
        subprocess.Popen(
            [node, 'server.js'],
            cwd=folder,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
        )
    except Exception:
        return False

    # Esperar a que responda (máx. ~6 segundos).
    for _ in range(20):
        time.sleep(0.3)
        if _server_activo(url):
            return True
    return False


def solicitar_pin(email: str) -> str:
    """
    Pide al servidor Node el PIN de recuperación para `email`.

    Si el servidor no responde, intenta levantarlo automáticamente y reintenta.
    Devuelve el PIN (str) o lanza una excepción si no se pudo obtener.
    """
    url = f"{Config.NODE_RECUPERACION_URL}/recuperar"

    if not _server_activo(url):
        if not _iniciar_server(url):
            raise RuntimeError('No se pudo iniciar el servidor Node de recuperación.')

    # Timeout algo mayor por si el correo tarda en salir.
    resp = requests.post(url, json={'email': email}, timeout=15)
    resp.raise_for_status()
    pin = resp.json().get('pin')
    if not pin:
        raise RuntimeError('El servidor Node no devolvió un PIN.')
    return str(pin)
