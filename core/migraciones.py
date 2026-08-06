"""
Migraciones automáticas de la base de datos.

La aplicación es autocontenida: al iniciar (o al visitar ciertas secciones)
garantiza que las tablas, columnas y datos iniciales que necesita existan.
Esto evita errores de "tabla no existe" al desplegar en una base nueva.

Todas las funciones de este módulo son idempotentes: se pueden ejecutar
varias veces sin efectos secundarios.
"""

from werkzeug.security import generate_password_hash

from config import Config
from database_handler import obtener_db


def asegurar_cuenta_dueño():
    """
    Asegura que el email definido en ADMIN_EMAIL exista como administrador
    dueño en la tabla `usuarios`.

    - Agrega la columna `es_dueño` si no existe.
    - Si ya existe una tabla legacy `admin_config` (login anterior del panel),
      migra su contraseña a la cuenta del dueño para no perder la que el
      dueño ya conoce, y luego elimina la tabla legacy.
    - Si la cuenta no existe, la crea con la contraseña ADMIN_PASSWORD.
    """
    db = obtener_db()
    cursor = db.cursor(dictionary=True)

    # Columna que identifica al dueño del panel.
    cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'es_dueño'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE usuarios ADD COLUMN es_dueño TINYINT(1) DEFAULT 0")

    # Credenciales legacy del panel (por si ya existían de versiones anteriores).
    hash_legacy = None
    try:
        cursor.execute("SELECT email, password_hash FROM admin_config")
        for fila in cursor.fetchall():
            if fila['email'] == Config.ADMIN_EMAIL:
                hash_legacy = fila['password_hash']
    except Exception:
        pass  # La tabla legacy ya no existe: nada que migrar.

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (Config.ADMIN_EMAIL,))
    dueño = cursor.fetchone()
    if dueño:
        cursor.execute(
            "UPDATE usuarios SET rol = 'admin', activo = 1, es_dueño = 1 WHERE email = %s",
            (Config.ADMIN_EMAIL,))
        if hash_legacy:
            cursor.execute(
                "UPDATE usuarios SET password = %s WHERE email = %s",
                (hash_legacy, Config.ADMIN_EMAIL))
    else:
        cursor.execute(
            """INSERT INTO usuarios (nombre, apellido, email, password, rol, activo, es_dueño)
               VALUES (%s, %s, %s, %s, 'admin', 1, 1)""",
            ('Fabricio', '', Config.ADMIN_EMAIL,
             hash_legacy or generate_password_hash(Config.ADMIN_PASSWORD)))

    # La tabla legacy ya no se usa para autenticar: eliminarla.
    cursor.execute("DROP TABLE IF EXISTS admin_config")
    db.commit()


def asegurar_tabla_orientaciones():
    """
    Crea la tabla de orientaciones (y la puente carrera_areas) si no existen
    y las llena con las áreas actuales de las carreras. Así el filtro público
    de "Carreras" nunca queda vacío.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orientaciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrera_areas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            carrera_id INT NOT NULL,
            area VARCHAR(100) NOT NULL,
            INDEX idx_carrera (carrera_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("""
        INSERT IGNORE INTO orientaciones (nombre)
        SELECT DISTINCT area_profesional FROM carreras
        WHERE area_profesional IS NOT NULL AND area_profesional <> ''
    """)
    db.commit()


def obtener_areas_carrera(carrera_id: int) -> list:
    """Devuelve la lista de áreas/orientaciones asignadas a una carrera."""
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT area FROM carrera_areas WHERE carrera_id = %s ORDER BY id",
        (carrera_id,)
    )
    return [r['area'] for r in cursor.fetchall()]


def guardar_areas_carrera(carrera_id: int, areas: list) -> None:
    """
    Reemplaza las áreas de una carrera por la lista dada y asegura que cada
    una exista también como orientación (para el filtro público).
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM carrera_areas WHERE carrera_id = %s", (carrera_id,))
    areas = [a.strip() for a in areas if a and a.strip()]
    for area in areas:
        cursor.execute("INSERT IGNORE INTO orientaciones (nombre) VALUES (%s)", (area,))
        cursor.execute(
            "INSERT INTO carrera_areas (carrera_id, area) VALUES (%s, %s)",
            (carrera_id, area)
        )
    db.commit()


def asegurar_tabla_fuentes():
    """
    Crea la tabla de fuentes si no existe, le agrega la columna `activo` y
    registra automáticamente las fuentes que ya están en las noticias, salvo
    las que fueron eliminadas a propósito (registradas en fuentes_eliminadas).
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuentes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SHOW COLUMNS FROM fuentes LIKE 'activo'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE fuentes ADD COLUMN activo TINYINT(1) DEFAULT 1")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuentes_eliminadas (
            nombre VARCHAR(100) NOT NULL PRIMARY KEY
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT nombre FROM fuentes_eliminadas")
    eliminadas = {r[0] for r in cursor.fetchall()}
    # Registra las fuentes de las noticias que todavía no están eliminadas.
    cursor.execute("SELECT DISTINCT fuente FROM noticias WHERE fuente IS NOT NULL AND fuente <> ''")
    for (nombre,) in cursor.fetchall():
        if nombre not in eliminadas:
            cursor.execute("INSERT IGNORE INTO fuentes (nombre) VALUES (%s)", (nombre,))
    db.commit()


def asegurar_tabla_filtros_fecha():
    """
    Crea la tabla de filtros de fecha del buscador de noticias y asegura los
    filtros predefinidos (Hoy, Ayer, Esta semana, Este mes, Todas).

    Cada filtro guarda su etiqueta y la condición SQL que se usa al filtrar,
    de modo que el admin puede agregar sus propios rangos de fecha.
    """
    db = obtener_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filtros_fecha (
            id INT AUTO_INCREMENT PRIMARY KEY,
            valor VARCHAR(30) NOT NULL UNIQUE,
            etiqueta VARCHAR(50) NOT NULL,
            condicion VARCHAR(250) NOT NULL DEFAULT '',
            activo TINYINT(1) DEFAULT 1,
            orden INT DEFAULT 0,
            es_fijo TINYINT(1) DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    # Backfill de columnas agregadas en versiones posteriores.
    for col, ddl in [
        ('condicion', "ADD COLUMN condicion VARCHAR(250) NOT NULL DEFAULT ''"),
        ('es_fijo', 'ADD COLUMN es_fijo TINYINT(1) DEFAULT 0'),
    ]:
        cursor.execute(f"SHOW COLUMNS FROM filtros_fecha LIKE '{col}'")
        if not cursor.fetchone():
            cursor.execute(f"ALTER TABLE filtros_fecha {ddl}")

    # Si la tabla está vacía, inserta los filtros predefinidos.
    cursor.execute("SELECT COUNT(*) AS n FROM filtros_fecha")
    if cursor.fetchone()['n'] == 0:
        presets = [
            ('todas', 'Todas', '', 1, 0, 1),
            ('hoy', 'Hoy', 'fecha = CURDATE()', 1, 1, 1),
            ('ayer', 'Ayer', 'fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)', 1, 2, 1),
            ('semana', 'Esta semana', 'fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)', 1, 3, 1),
            ('mes', 'Este mes', 'fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)', 1, 4, 1),
        ]
        cursor.executemany(
            "INSERT INTO filtros_fecha (valor, etiqueta, condicion, activo, orden, es_fijo) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            presets
        )

    # Backfill: asegura que los filtros predefinidos tengan su condición y no
    # puedan borrarse desde el panel.
    backfill = {
        'todas': '',
        'hoy': 'fecha = CURDATE()',
        'ayer': 'fecha = DATE_SUB(CURDATE(), INTERVAL 1 DAY)',
        'semana': 'fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)',
        'mes': 'fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)',
    }
    for valor, cond in backfill.items():
        cursor.execute(
            "UPDATE filtros_fecha SET condicion = %s, es_fijo = 1 WHERE valor = %s",
            (cond, valor))
    db.commit()


def asegurar_columnas_botones_game(db, cursor):
    """
    Agrega las columnas de texto de los botones del juego "Descubre tu Carrera"
    a la tabla game_carreras si no existen (migración de versiones anteriores).
    """
    columnas = {
        'boton_no': "ADD COLUMN boton_no VARCHAR(100) NOT NULL DEFAULT 'No es lo mío'",
        'boton_info': "ADD COLUMN boton_info VARCHAR(100) NOT NULL DEFAULT 'Info'",
        'boton_yes': "ADD COLUMN boton_yes VARCHAR(100) NOT NULL DEFAULT 'Me interesa'",
    }
    cursor.execute("SHOW COLUMNS FROM game_carreras")
    filas = cursor.fetchall()
    existentes = {r['Field'] if isinstance(r, dict) else r[0] for r in filas}
    for nombre, ddl in columnas.items():
        if nombre not in existentes:
            cursor.execute(f"ALTER TABLE game_carreras {ddl}")
            existentes.add(nombre)
    db.commit()
