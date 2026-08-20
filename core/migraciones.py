"""
Migraciones automáticas de la base de datos.

La aplicación es autocontenida: al iniciar (o al visitar ciertas secciones)
garantiza que las tablas, columnas y datos iniciales que necesita existan.
Esto evita errores de "tabla no existe" al desplegar en una base nueva.

Todas las funciones de este módulo son idempotentes: se pueden ejecutar
varias veces sin efectos secundarios.
"""

import io
import os
import re

from werkzeug.security import generate_password_hash

from config import Config
from database_handler import obtener_db

RUTA_DUMP = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'base de datos', 'futuro 360.sql')


def asegurar_tabla_usuarios():
    """
    Crea la tabla `usuarios` si no existe.

    Cada máquina tiene sus propias cuentas (el contenido compartido no incluye
    usuarios): la del dueño/admin se crea con asegurar_cuenta_dueño y las
    demás, por el registro del sitio.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único del usuario',
            nombre VARCHAR(100) NOT NULL COMMENT 'Nombre de pila',
            apellido VARCHAR(100) DEFAULT NULL COMMENT 'Apellido (opcional)',
            email VARCHAR(150) NOT NULL COMMENT 'Correo electrónico, único, usado para login y recuperación',
            password VARCHAR(255) NOT NULL COMMENT 'Hash de la contraseña (Werkzeug)',
            rol ENUM('usuario','admin') DEFAULT 'usuario' COMMENT 'Rol de acceso: usuario o admin',
            activo TINYINT(1) DEFAULT 1 COMMENT '1 = habilitado, 0 = deshabilitado',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de alta',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Última actualización',
            es_dueño TINYINT(1) DEFAULT 0 COMMENT '1 = dueño del panel (permisos exclusivos)',
            PRIMARY KEY (id),
            UNIQUE KEY email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='Cuentas del sistema: visitantes registrados, administradores y el dueño'
    """)
    db.commit()


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

    # Seguridad: si la tabla aún no existe, crearla primero.
    asegurar_tabla_usuarios()

    # Columna que identifica al dueño del panel.
    cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'es_dueño'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE usuarios ADD COLUMN es_dueño TINYINT(1) DEFAULT 0")

    # Credenciales legacy del panel (por si ya existían de versiones anteriores).
    # SEGURIDAD: las contraseñas SIEMPRE se guardan hasheadas con
    # generate_password_hash (Werkzeug). Nunca se escribe texto plano en la BD.
    # El hash_legacy de admin_config ya es un hash; si por cualquier motivo ese
    # valor no tiene formato de hash (p. ej. quedó texto plano de una versión
    # muy vieja), se regenera con generate_password_hash en vez de migrarlo.
    hash_legacy = None
    try:
        cursor.execute("SELECT email, password_hash FROM admin_config")
        for fila in cursor.fetchall():
            if fila['email'] == Config.ADMIN_EMAIL:
                legacy = fila['password_hash']
                if legacy and legacy.startswith(
                        ('scrypt:', 'pbkdf2:', 'sha256:', 'sha1:', 'md5:')):
                    hash_legacy = legacy
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
        nombre_dueño = Config.ADMIN_EMAIL.split('@')[0] or 'Dueño'
        cursor.execute(
            """INSERT INTO usuarios (nombre, apellido, email, password, rol, activo, es_dueño)
               VALUES (%s, %s, %s, %s, 'admin', 1, 1)""",
            (nombre_dueño, '', Config.ADMIN_EMAIL,
             hash_legacy or generate_password_hash(Config.ADMIN_PASSWORD)))

    # La tabla legacy ya no se usa para autenticar: eliminarla.
    cursor.execute("DROP TABLE IF EXISTS admin_config")
    db.commit()


def asegurar_columnas_esquema():
    """
    Asegura que las tablas del esquema base tengan todas las columnas que la
    aplicación usa. Las columnas agregadas en versiones posteriores al dump
    (popular, imagen_portada, a_que_se_dedica, apellido, activo, created_at,
    es_dueño, completado, area_id, puntaje) se agregan al vuelo si no existen.

    Idempotente: se puede ejecutar en cada arranque sin efectos secundarios.
    """
    db = obtener_db()
    cursor = db.cursor()

    columnas = {
        'usuarios': {
            'apellido': "ADD COLUMN apellido VARCHAR(100) DEFAULT NULL",
            'activo': "ADD COLUMN activo TINYINT(1) DEFAULT 1",
            'created_at': "ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
            'es_dueño': "ADD COLUMN es_dueño TINYINT(1) DEFAULT 0",
        },
        'carreras': {
            'popular': "ADD COLUMN popular TINYINT(1) DEFAULT 0",
            'imagen_portada': "ADD COLUMN imagen_portada VARCHAR(500) DEFAULT NULL",
            'imagen_principal': "ADD COLUMN imagen_principal VARCHAR(500) DEFAULT NULL",
            'a_que_se_dedica': "ADD COLUMN a_que_se_dedica TEXT DEFAULT NULL",
            'video': "ADD COLUMN video VARCHAR(500) DEFAULT NULL",
        },
        'noticias': {
            'video': "ADD COLUMN video VARCHAR(500) DEFAULT NULL",
        },
        'tests': {
            'completado': "ADD COLUMN completado TINYINT(1) DEFAULT 0",
        },
        'resultados': {
            'area_id': "ADD COLUMN area_id INT DEFAULT NULL",
            'puntaje': "ADD COLUMN puntaje INT DEFAULT 0",
        },
    }

    for tabla, cols in columnas.items():
        try:
            cursor.execute(f"SHOW COLUMNS FROM {tabla}")
            existentes = {r[0] for r in cursor.fetchall()}
        except Exception as e:
            print(f'[esquema] Tabla {tabla} no disponible: {e}')
            continue
        for nombre, ddl in cols.items():
            if nombre in existentes:
                continue
            try:
                cursor.execute(f"ALTER TABLE {tabla} {ddl}")
                existentes.add(nombre)
                print(f'[esquema] Columna agregada: {tabla}.{nombre}')
            except Exception as e:
                print(f'[esquema] Error al agregar {tabla}.{nombre}: {e}')

    db.commit()


def asegurar_datos_iniciales():
    """
    Reproduce de forma idempotente los datos iniciales que antes vivían en
    migraciones manuales, para que una base recién importada quede idéntica
    a la de desarrollo:

    - Agrega la opción "Ninguna de las anteriores" (área Neutral) a cada
      pregunta que no la tenga.
    - Marca como `popular` las carreras destacadas del catálogo.
    """
    db = obtener_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO opciones_pregunta (pregunta_id, texto_opcion, area_profesional)
            SELECT id, 'Ninguna de las anteriores', 'Neutral'
            FROM preguntas
            WHERE id NOT IN (
                SELECT DISTINCT pregunta_id FROM opciones_pregunta
                WHERE texto_opcion = 'Ninguna de las anteriores'
            )
        """)
    except Exception as e:
        print(f'[datos] Error al insertar opción neutral: {e}')

    try:
        cursor.execute("SELECT COUNT(*) FROM carreras WHERE popular = 1")
        hay_populares = cursor.fetchone()[0] > 0
    except Exception:
        # Si no se puede consultar, no sobreescribir lo que eligió el admin.
        hay_populares = True

    # El seed de carreras destacadas solo corre la primera vez (cuando todavía
    # no hay ninguna), para no pisar las selecciones del panel de administración.
    if not hay_populares:
        try:
            cursor.execute("""
                UPDATE carreras SET popular = 1 WHERE nombre IN (
                    'Ingeniería en Sistemas de Información',
                    'Medicina',
                    'Psicología',
                    'Abogacía',
                    'Contador Público Nacional',
                    'Ingeniería Civil',
                    'Licenciatura en Administración',
                    'Diseño Gráfico'
                )
            """)
        except Exception as e:
            print(f'[datos] Error al marcar carreras populares: {e}')

    db.commit()


def asegurar_contenido_referencia():
    """
    Hace que una base quede igual a la del desarrollador con solo `git pull` +
    arrancar la app, sin importar dumps a mano.

    Usa `base de datos/futuro 360.sql` como única fuente de verdad y, para las
    tablas de contenido (carreras, noticias, fuentes, preguntas del juego...):

    - si la tabla NO existe, la crea (esquema del dump) y le carga sus datos;
    - si existe pero está VACÍA, solo le carga los datos;
    - si existe y tiene registros, NO la toca (nunca pisa cambios locales).

    También crea cualquier otra tabla de esquema del dump que falte (tests,
    resultados, etc.) para que la base quede completa. Idempotente.
    """
    db = obtener_db()
    cursor = db.cursor()

    if not os.path.exists(RUTA_DUMP):
        print('[base] dump futuro 360.sql no encontrado; sin auto-bootstrap')
        return

    # --- Lectura del dump: acumula los bloques CREATE TABLE (multilínea)
    # --- hasta su ';' final y las sentencias INSERT (una por línea).
    creaciones = {}
    inserciones = {}
    acumulando = None
    for ln in io.open(RUTA_DUMP, 'r', encoding='utf-8'):
        s = ln.strip()
        if not s or s.startswith('--'):
            continue
        if s.startswith('CREATE TABLE'):
            m = re.match(r"CREATE TABLE `([A-Za-z0-9_]+)`", s)
            if m:
                acumulando = [s]
                creaciones[m.group(1)] = acumulando
            continue
        if acumulando is not None:
            acumulando.append(s)
            if s.endswith(';'):
                acumulando = None
            continue
        if s.startswith('INSERT INTO'):
            m = re.match(r"INSERT INTO `([A-Za-z0-9_]+)`", s)
            if m:
                inserciones.setdefault(m.group(1), []).append(s)
    creaciones = {t: '\n'.join(bloque) for t, bloque in creaciones.items()}

    # --- Estado actual de cada tabla que el dump define.
    estado = {}
    for tabla in creaciones:
        try:
            cursor.execute("SELECT COUNT(*) FROM `%s`" % tabla)
            estado[tabla] = cursor.fetchone()[0]
        except Exception:
            estado[tabla] = None  # no existe todavía

    faltantes = [t for t, n in estado.items() if n is None]
    vacias = [t for t, n in estado.items() if n == 0]
    if not faltantes and not vacias:
        print('[base] Esquema y contenido de referencia ya presentes')
        return

    try:
        cursor.execute('SET FOREIGN_KEY_CHECKS=0')

        # Crear tablas que no existen (todas las del dump: content + vacías).
        creadas = 0
        for tabla in faltantes:
            cursor.execute(creaciones[tabla])
            creadas += 1

        # Sembrar datos solo en las tablas que quedaron sin contenido.
        sembradas = 0
        for tabla in faltantes + vacias:
            for insert in inserciones.get(tabla, []):
                cursor.execute(insert)
                sembradas += 1

        cursor.execute('SET FOREIGN_KEY_CHECKS=1')
        db.commit()

        if creadas:
            print(f'[base] Tablas creadas: {", ".join(faltantes)}')
        if sembradas:
            print(f'[seed] {sembradas} registros sembrados en: '
                  f'{", ".join(vacias)}'
                  if vacias else f'[seed] {sembradas} registros sembrados')
    except Exception as e:
        db.rollback()
        print(f'[base] Error al preparar contenido de referencia: {e}')


def condicion_fecha_segura(condicion) -> bool:
    """
    Valida que una condición SQL de filtrado de noticias sea segura para
    concatenar en un query (whitelist estricta por expresión regular).

    SOLO se permiten condiciones que operan sobre la columna `fecha` con:
      - operadores de comparación (=, >=, <=, >, <),
      - una fecha literal 'YYYY-MM-DD',
      - CURDATE() o DATE_SUB(CURDATE(), INTERVAL N DAY) (presets fijos),
      - y como máximo un AND con otra fecha literal (rango definido por el
        admin en el panel, p. ej. "fecha >= '2024-01-01' AND fecha <= '2024-12-31'").

    Cualquier otra construcción (subqueries, UNION, funciones arbitrarias,
    más de una AND, etc.) se rechaza. Así la condición guardada en la BD por
    un admin nunca puede convertirse en inyección SQL.
    """
    if not condicion or not isinstance(condicion, str):
        return False
    import re
    return bool(re.fullmatch(
        r"fecha\s*(>=|<=|=|>|<)\s*"
        r"('[0-9]{4}-[0-9]{2}-[0-9]{2}'|CURDATE\(\)"
        r"|DATE_SUB\(CURDATE\(\), INTERVAL [0-9]+ DAY\))"
        r"(\s+AND\s+fecha\s*(>=|<=|=|>|<)\s*'[0-9]{4}-[0-9]{2}-[0-9]{2}')?",
        condicion.strip()))


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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la orientación',
            nombre VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nombre del área/orientación profesional'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Áreas/orientaciones de agrupación de carreras gestionables desde el panel'
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrera_areas (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la relación',
            carrera_id INT NOT NULL COMMENT 'Carrera asociada (FK → carreras.id)',
            area VARCHAR(100) NOT NULL COMMENT 'Área/orientación asignada a la carrera',
            INDEX idx_carrera (carrera_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Tabla puente entre carreras y áreas'
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la noticia',
            titulo VARCHAR(300) NOT NULL COMMENT 'Título de la noticia',
            descripcion TEXT DEFAULT NULL COMMENT 'Resumen o cuerpo de la noticia',
            imagen VARCHAR(500) DEFAULT NULL COMMENT 'Imagen (ruta local o URL de Cloudinary)',
            fuente VARCHAR(100) NOT NULL COMMENT 'Fuente (nombre del medio)',
            fecha DATE NOT NULL COMMENT 'Fecha de la noticia',
            link VARCHAR(500) DEFAULT '#' COMMENT 'Enlace de origen (único)',
            categoria VARCHAR(100) DEFAULT 'General' COMMENT 'Categoría de la noticia',
            es_externa TINYINT(1) DEFAULT 0 COMMENT '1 = redirige al link externo',
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de alta',
            UNIQUE KEY unique_link (link(255))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='Noticias educativas mostradas en la sección de noticias'
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la fuente',
            nombre VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nombre de la fuente (único)'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Fuentes de noticias disponibles'
    """)
    cursor.execute("SHOW COLUMNS FROM fuentes LIKE 'activo'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE fuentes ADD COLUMN activo TINYINT(1) DEFAULT 1")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuentes_eliminadas (
            nombre VARCHAR(100) NOT NULL PRIMARY KEY COMMENT 'Nombre de la fuente eliminada (evita que reingrese)'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Registro de fuentes dadas de baja a propósito'
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador del filtro',
            valor VARCHAR(30) NOT NULL UNIQUE COMMENT 'Valor interno del filtro',
            etiqueta VARCHAR(50) NOT NULL COMMENT 'Texto visible del filtro',
            condicion VARCHAR(250) NOT NULL DEFAULT '' COMMENT 'Condición SQL de filtrado sobre la fecha',
            activo TINYINT(1) DEFAULT 1 COMMENT '1 = habilitado',
            orden INT DEFAULT 0 COMMENT 'Orden de aparición',
            es_fijo TINYINT(1) DEFAULT 0 COMMENT '1 = no editable desde el panel'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Filtros de tiempo del buscador de noticias'
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la tarjeta',
            carrera_id INT NOT NULL COMMENT 'Carrera asociada (FK → carreras.id)',
            texto_boton VARCHAR(100) DEFAULT 'Ver carrera' COMMENT 'Texto del botón de la tarjeta',
            titulo_card VARCHAR(150) COMMENT 'Título que se muestra en la tarjeta',
            descripcion_card TEXT COMMENT 'Descripción de la tarjeta',
            activo TINYINT(1) DEFAULT 1 COMMENT '1 = visible en el juego',
            orden INT DEFAULT 0 COMMENT 'Orden de aparición',
            boton_no VARCHAR(100) NOT NULL DEFAULT 'No es lo mío' COMMENT 'Texto del botón "No"',
            boton_info VARCHAR(100) NOT NULL DEFAULT 'Info' COMMENT 'Texto del botón "Info"',
            boton_yes VARCHAR(100) NOT NULL DEFAULT 'Me interesa' COMMENT 'Texto del botón "Me interesa"',
            INDEX idx_carrera (carrera_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Carreras que participan en el juego de descubrimiento'
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
            user_id INT NOT NULL PRIMARY KEY COMMENT 'Usuario con actividad reciente (FK → usuarios.id)',
            last_seen DATETIME NOT NULL COMMENT 'Última fecha/hora de actividad registrada'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        COMMENT='Presencia en línea: una fila por usuario logueado (usuarios en línea)'
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la pregunta',
            texto_pregunta VARCHAR(300) NOT NULL COMMENT 'Enunciado de la pregunta',
            opcion_a_texto VARCHAR(200) NOT NULL COMMENT 'Texto de la opción A',
            opcion_a_area VARCHAR(100) NOT NULL COMMENT 'Área que suma la opción A',
            opcion_b_texto VARCHAR(200) NOT NULL COMMENT 'Texto de la opción B',
            opcion_b_area VARCHAR(100) NOT NULL COMMENT 'Área que suma la opción B',
            activo TINYINT(1) DEFAULT 1 COMMENT '1 = visible en el juego',
            orden INT DEFAULT 0 COMMENT 'Orden de aparición',
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de alta'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='Preguntas del juego "Descubre tu Carrera"'
    """)
    db.commit()


def asegurar_tabla_password_resets():
    """
    Crea la tabla `password_resets` si no existe. Guarda los códigos PIN de
    recuperación de contraseña.

    El PIN se guarda HASHEADO (werkzeug: scrypt/pbkdf2), no en claro, por eso
    la columna `codigo` es VARCHAR(255) y no VARCHAR(6).
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador del registro',
            email VARCHAR(255) NOT NULL COMMENT 'Email del usuario (FK lógica → usuarios.email)',
            codigo VARCHAR(255) NOT NULL COMMENT 'Hash del código PIN (werkzeug, no en claro)',
            usado TINYINT(1) DEFAULT 0 COMMENT '1 = código ya utilizado',
            expira_en DATETIME NOT NULL COMMENT 'Fecha de expiración del código',
            fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación',
            KEY idx_email (email),
            KEY idx_codigo (codigo)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='Códigos PIN de recuperación de contraseña (hash)'
    """)
    # Migración para bases ya creadas: la columna solía ser VARCHAR(6) (PIN en
    # claro). Ahora guardamos el hash, que no entra en 6 caracteres.
    try:
        cursor.execute(
            "ALTER TABLE password_resets MODIFY COLUMN codigo VARCHAR(255) "
            "NOT NULL COMMENT 'Hash del código PIN (werkzeug, no en claro)'")
    except Exception:
        # La columna ya tiene el tamaño correcto o la tabla no existía aún.
        pass
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador del comentario',
            nombre VARCHAR(100) DEFAULT NULL COMMENT 'Nombre del remitente',
            email VARCHAR(100) DEFAULT NULL COMMENT 'Email del remitente',
            mensaje TEXT DEFAULT NULL COMMENT 'Contenido del mensaje',
            fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de envío'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='Mensajes enviados desde el formulario de contacto'
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
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador del área',
            nombre VARCHAR(100) NOT NULL COMMENT 'Nombre del área profesional',
            descripcion TEXT DEFAULT NULL COMMENT 'Descripción del área',
            icono VARCHAR(50) DEFAULT NULL COMMENT 'Ícono asociado',
            color VARCHAR(20) DEFAULT NULL COMMENT 'Color representativo'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='Áreas profesionales del test y de las carreras'
    """)
    db.commit()
