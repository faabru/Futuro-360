"""
Protección contra fuerza bruta: 5 intentos fallidos por email,
bloqueo de 15 min. Persistido en MySQL (sobrevive reinicios).
"""

from database_handler import obtener_db

MAX_INTENTOS = 5
MINUTOS_BLOQUEO = 15


def asegurar_tabla_intentos():
    """Crea la tabla de intentos si no existe (idempotente)."""
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intentos_login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            accion VARCHAR(30) NOT NULL COMMENT 'Flujo protegido: login, admin_login, codigo_sitio, codigo_admin',
            email VARCHAR(150) NOT NULL COMMENT 'Email o clave del intento',
            intentos INT DEFAULT 0 COMMENT 'Intentos fallidos consecutivos',
            bloqueado_hasta DATETIME DEFAULT NULL COMMENT 'Hasta cuándo está bloqueado',
            ultimo_intento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_accion_email (accion, email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Límite de intentos para login y códigos de recuperación'
    """)
    db.commit()


def _registro(accion: str, email: str):
    """Devuelve la fila de intentos del (accion, email) o None si no existe."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM intentos_login WHERE accion = %s AND email = %s",
        (accion, email))
    return cursor.fetchone()


def permite_intento(accion: str, email: str) -> bool:
    """True si (accion, email) todavía puede intentar (no está bloqueado)."""
    asegurar_tabla_intentos()
    fila = _registro(accion, email)
    if not fila or not fila.get('bloqueado_hasta'):
        return True
    # Si el bloqueo ya venció, se permite intentar de nuevo.
    return fila['bloqueado_hasta'] <= __import__('datetime').datetime.now()


def registrar_fallo(accion: str, email: str) -> None:
    """Registra un intento fallido. Al alcanzar MAX_INTENTOS bloquea el email."""
    asegurar_tabla_intentos()
    db = obtener_db()
    cursor = db.cursor()
    fila = _registro(accion, email)
    if not fila:
        cursor.execute(
            "INSERT INTO intentos_login (accion, email, intentos) VALUES (%s, %s, 1)",
            (accion, email))
    else:
        intentos = fila['intentos'] + 1
        if intentos >= MAX_INTENTOS:
            cursor.execute(
                "UPDATE intentos_login SET intentos = %s, "
                "bloqueado_hasta = DATE_ADD(NOW(), INTERVAL %s MINUTE), "
                "ultimo_intento = NOW() WHERE id = %s",
                (intentos, MINUTOS_BLOQUEO, fila['id']))
        else:
            cursor.execute(
                "UPDATE intentos_login SET intentos = %s, "
                "bloqueado_hasta = NULL, ultimo_intento = NOW() WHERE id = %s",
                (intentos, fila['id']))
    db.commit()


def registrar_exito(accion: str, email: str) -> None:
    """Borra el registro de intentos tras un intento exitoso."""
    asegurar_tabla_intentos()
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM intentos_login WHERE accion = %s AND email = %s",
        (accion, email))
    db.commit()


def minutos_restantes_bloqueo(accion: str, email: str) -> int:
    """Minutos que faltan para que venza el bloqueo (0 si no está bloqueado)."""
    fila = _registro(accion, email)
    if not fila or not fila.get('bloqueado_hasta'):
        return 0
    from datetime import datetime
    restante = (fila['bloqueado_hasta'] - datetime.now()).total_seconds()
    return max(0, int(restante // 60) + 1)
