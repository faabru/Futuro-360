"""
Cliente del servidor Node de recuperación de contraseña.

El prototipo Node ("recuperacion de contraseña/server.js") genera el PIN y
lo envía por Resend. Este módulo le pide el PIN a ese servidor y, si no está
activo, lo levanta automáticamente (subprocess) para que la recuperación
funcione sin pasos manuales.
"""

import os
import shutil
import subprocess
import time

import requests

from config import Config

RUTA_FOLDER_NODE = 'recuperacion de contraseña'
# URL de Render interna: "https://futuro360-node.onrender.com" o el hostname
# privado (ej. "futuro360-node"). Se normaliza en _base_url().
NODE_RECUPERACION_URL = Config.NODE_RECUPERACION_URL


def _base_url() -> str:
    """Normaliza NODE_RECUPERACION_URL a una URL base con http(s)://."""
    url = (NODE_RECUPERACION_URL or 'http://localhost:3000').strip().rstrip('/')
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url


def _es_desarrollo() -> bool:
    """El auto-arranque local solo tiene sentido en desarrollo (localhost)."""
    url = _base_url()
    return ('localhost' in url) or ('127.0.0.1' in url)


def _server_activo(timeout: float = 1.0) -> bool:
    """Devuelve True si el servidor Node responde en /health."""
    try:
        requests.get(f"{_base_url()}/health", timeout=timeout)
        return True
    except Exception:
        return False


def _iniciar_server() -> bool:
    """
    Intenta levantar el servidor Node en background desde la carpeta del
    prototipo. Devuelve True si quedó respondiendo (o ya lo estaba).
    Solo se usa en desarrollo local (localhost), nunca contra un servicio
    remoto de Render.
    """
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
        if _server_activo():
            return True
    return False


def solicitar_pin(email: str) -> str:
    """
    Pide al servidor Node el PIN de recuperación para `email`.

    Si el servidor no responde y estamos en desarrollo local, intenta
    levantarlo automáticamente y reintenta. En producción (Render) el Node
    corre como servicio separado: si no responde, falla con un error claro.
    Devuelve el PIN (str) o lanza una excepción si no se pudo obtener.
    """
    url = f"{_base_url()}/recuperar"

    if not _server_activo():
        if _es_desarrollo() and not _iniciar_server():
            raise RuntimeError('No se pudo iniciar el servidor Node de recuperación.')
        if not _es_desarrollo():
            raise RuntimeError('El servidor Node de recuperación no está disponible.')

    # Timeout algo mayor por si el correo tarda en salir.
    resp = requests.post(url, json={'email': email}, timeout=15)
    resp.raise_for_status()
    pin = resp.json().get('pin')
    if not pin:
        raise RuntimeError('El servidor Node no devolvió un PIN.')
    return str(pin)
