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


def registrar_orientaciones(areas: list) -> None:
    """
    Registra áreas/orientaciones nuevas en la tabla `orientaciones` si no
    existen (idempotente). Se usa al guardar formularios donde el admin puede
    escribir un área a mano (preguntas, juego, noticias) para que esa área
    quede disponible en todos los dropdowns de las gestiones.
    """
    asegurar_tabla_orientaciones()
    db = obtener_db()
    cursor = db.cursor()
    for area in areas:
        nombre = area.strip()[:100] if area else ''
        if nombre:
            cursor.execute(
                "INSERT IGNORE INTO orientaciones (nombre) VALUES (%s)",
                (nombre,))
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


def asegurar_tabla_noticias():
    """
    Crea la tabla `noticias` si no existe. Es necesaria para la portada, la
    sección de noticias, las estadísticas del panel y la exportación a Excel.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(300) NOT NULL,
            descripcion TEXT DEFAULT NULL,
            imagen VARCHAR(500) DEFAULT NULL,
            fuente VARCHAR(100) NOT NULL,
            fecha DATE NOT NULL,
            link VARCHAR(500) DEFAULT '#',
            categoria VARCHAR(100) DEFAULT 'General',
            es_externa TINYINT(1) DEFAULT 0,
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_link (link(255))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    db.commit()


def asegurar_tabla_fuentes():
    """
    Crea la tabla de fuentes si no existe, le agrega la columna `activo` y
    registra automáticamente las fuentes que ya están en las noticias, salvo
    las que fueron eliminadas a propósito (registradas en fuentes_eliminadas).
    """
    asegurar_tabla_noticias()
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


def asegurar_tabla_game_carreras():
    """
    Crea la tabla `game_carreras` si no existe y registra en ella (backfill)
    todas las carreras del catálogo que todavía no tienen su tarjeta para el
    juego "Descubre tu Carrera".

    Es idempotente y no toca las tarjetas existentes, por lo que ejecutarlo en
    cada arranque o al abrir el panel garantiza que ninguna carrera quede fuera
    del juego ni se pierda. Las nuevas se agregan inactivas (el admin las activa
    desde el panel).
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_carreras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            carrera_id INT NOT NULL,
            texto_boton VARCHAR(100) DEFAULT 'Ver carrera',
            titulo_card VARCHAR(150),
            descripcion_card TEXT,
            activo TINYINT(1) DEFAULT 1,
            orden INT DEFAULT 0,
            boton_no VARCHAR(100) NOT NULL DEFAULT 'No es lo mío',
            boton_info VARCHAR(100) NOT NULL DEFAULT 'Info',
            boton_yes VARCHAR(100) NOT NULL DEFAULT 'Me interesa',
            INDEX idx_carrera (carrera_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    asegurar_columnas_botones_game(db, cursor)
    # Backfill: registra las carreras sin tarjeta en el juego.
    cursor.execute("""
        INSERT INTO game_carreras (carrera_id, titulo_card, descripcion_card, activo, orden)
        SELECT c.id, c.nombre, c.descripcion, 0, c.id
        FROM carreras c
        WHERE NOT EXISTS (
            SELECT 1 FROM game_carreras gc WHERE gc.carrera_id = c.id
        )
    """)
    db.commit()


def asegurar_tabla_sesiones_activas():
    """
    Crea la tabla `sesiones_activas` si no existe. Guarda, por cada usuario
    logueado, la última vez que se lo vio activo en el sitio, para poder
    mostrar "usuarios en línea" en tiempo real en el panel.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones_activas (
            user_id INT NOT NULL PRIMARY KEY,
            last_seen DATETIME NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    db.commit()


def asegurar_tabla_game_preguntas():
    """
    Crea la tabla `game_preguntas` si no existe. Guarda las preguntas del
    juego "Descubre tu Carrera".
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_preguntas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            texto_pregunta VARCHAR(300) NOT NULL,
            opcion_a_texto VARCHAR(200) NOT NULL,
            opcion_a_area VARCHAR(100) NOT NULL,
            opcion_b_texto VARCHAR(200) NOT NULL,
            opcion_b_area VARCHAR(100) NOT NULL,
            activo TINYINT(1) DEFAULT 1,
            orden INT DEFAULT 0,
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    db.commit()


def asegurar_tabla_password_resets():
    """
    Crea la tabla `password_resets` si no existe. Guarda los códigos PIN de
    recuperación de contraseña.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            codigo VARCHAR(6) NOT NULL,
            usado TINYINT(1) DEFAULT 0,
            expira_en DATETIME NOT NULL,
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            KEY idx_email (email),
            KEY idx_codigo (codigo)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    db.commit()


def asegurar_tabla_comentarios():
    """
    Crea la tabla `comentarios` si no existe. Guarda los mensajes enviados
    desde el formulario de contacto.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) DEFAULT NULL,
            email VARCHAR(100) DEFAULT NULL,
            mensaje TEXT DEFAULT NULL,
            fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    db.commit()


def asegurar_tabla_areas():
    """
    Crea la tabla `areas` si no existe. Se usa en las estadísticas del panel
    (usuarios por área profesional sugerida).
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT DEFAULT NULL,
            icono VARCHAR(50) DEFAULT NULL,
            color VARCHAR(20) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    db.commit()
