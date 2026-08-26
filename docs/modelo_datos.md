# Modelo de Datos — Futuro 360

Base de datos relacional **MySQL** (`futuro360`). Este documento describe el modelo entidad/relación,
la referencia de tablas y las relaciones entre entidades.

---

## ¿Qué es el modelo de datos?

El modelo de datos es el **plano de la base de datos**. Define:
- Qué tablas existen (cada tabla es como una hoja de cálculo)
- Qué campos tiene cada tabla (cada columna)
- Cómo se relacionan entre sí (qué tablas se conectan y por qué)

**En términos simples:** es la estructura que organiza toda la información del sistema.

---

## Diagrama entidad/relación

### Versión Mermaid (se renderiza en GitHub)

```mermaid
erDiagram
    USUARIOS     ||--o{ TESTS              : "realiza"
    TESTS        ||--o| RESULTADOS         : "genera"
    TESTS        ||--o{ RESPUESTAS         : "contiene"
    PREGUNTAS    ||--o{ OPCIONES           : "tiene"
    AREAS        ||--o{ OPCIONES           : "categoriza"
    PREGUNTAS    ||--o{ OPCIONES_PREGUNTA  : "tiene (legacy)"
    AREAS        ||--o{ RESULTADOS         : "sugiere"
    CARRERAS     ||--o{ GAME_CARRERAS      : "participa en"
    RESPUESTAS   }o--|| PREGUNTAS          : "refiere a"
    RESPUESTAS   }o--|| OPCIONES           : "selecciona"
    PASSWORD_RESETS }o--|| USUARIOS        : "recupera"
    USUARIOS     ||--o| SESIONES_ACTIVAS   : "presencia en línea"
    CARRERAS     ||--o{ CARRERA_AREAS      : "se clasifica"
    AREAS        ||--o{ CARRERA_AREAS      : "agrupa"
    CARRERAS     ||--o{ CARRERA_UNIVERSIDAD: "se dicta en"
    UNIVERSIDADES ||--o{ CARRERA_UNIVERSIDAD: "dicta"

    USUARIOS {
        int id PK
        varchar nombre
        varchar apellido
        varchar email UK
        varchar password
        enum rol
        tinyint activo
        datetime created_at
        datetime updated_at
        tinyint es_dueño
    }

    TESTS {
        int id PK
        int usuario_id FK
        datetime fecha
        tinyint completado
        timestamp fecha_realizacion
    }

    RESULTADOS {
        int id PK
        int test_id FK UK
        int area_id FK
        varchar area_profesional_sugerida
        int puntaje
        longtext detalle
        datetime created_at
        text notas_personales
    }

    RESPUESTAS {
        int id PK
        int test_id FK
        int pregunta_id FK
        int opcion_id FK
    }

    PREGUNTAS {
        int id PK
        varchar texto_pregunta
        varchar area_profesional
    }

    OPCIONES {
        int id PK
        int pregunta_id FK
        int area_id FK
        varchar texto
        int puntaje
    }

    OPCIONES_PREGUNTA {
        int id PK
        int pregunta_id FK
        varchar texto_opcion
        varchar area_profesional
    }

    AREAS {
        int id PK
        varchar nombre
        text descripcion
        varchar icono
        varchar color
    }

    CARRERAS {
        int id PK
        varchar nombre
        text descripcion
        varchar area_profesional
        text instituciones
        tinyint popular
        varchar imagen
        varchar imagen_portada
        varchar imagen_principal
        varchar video
        text a_que_se_dedica
    }

    CARRERA_AREAS {
        int id PK
        int carrera_id FK
        varchar area
    }

    UNIVERSIDADES {
        int id PK
        varchar nombre UK
        varchar siglas
        enum tipo
        varchar sitio_web
        tinyint activo
    }

    CARRERA_UNIVERSIDAD {
        int carrera_id PK FK
        int universidad_id PK FK
    }

    GAME_CARRERAS {
        int id PK
        int carrera_id FK
        varchar texto_boton
        varchar titulo_card
        text descripcion_card
        tinyint activo
        int orden
    }

    GAME_PREGUNTAS {
        int id PK
        varchar texto_pregunta
        varchar opcion_a_texto
        varchar opcion_a_area
        varchar opcion_b_texto
        varchar opcion_b_area
        tinyint activo
        int orden
        timestamp fecha_creacion
    }

    NOTICIAS {
        int id PK
        varchar titulo
        text descripcion
        varchar imagen
        varchar video
        varchar fuente
        date fecha
        varchar link UK
        varchar categoria
        tinyint es_externa
        timestamp fecha_creacion
    }

    FUENTES {
        int id PK
        varchar nombre UK
        tinyint activo
    }

    FILTROS_FECHA {
        int id PK
        varchar valor UK
        varchar etiqueta
        tinyint activo
        int orden
        varchar condicion
        tinyint es_fijo
    }

    ORIENTACIONES {
        int id PK
        varchar nombre UK
    }

    COMENTARIOS {
        int id PK
        varchar nombre
        varchar email
        text mensaje
        timestamp fecha
    }

    PASSWORD_RESETS {
        int id PK
        varchar email FK
        varchar codigo
        tinyint usado
        datetime expira_en
        timestamp fecha_creacion
    }

    SESIONES_ACTIVAS {
        int user_id PK FK
        datetime last_seen
    }

    FUENTES_ELIMINADAS {
        varchar nombre PK
    }
```

### Versión texto (legible en cualquier visor)

```
USUARIOS          1 ────< N  TESTS              (un usuario realiza varios tests)
TESTS             1 ────< 1  RESULTADOS         (un test genera un único resultado)
TESTS             1 ────< N  RESPUESTAS         (un test contiene las respuestas a varias preguntas)
PREGUNTAS         1 ────< N OPCIONES            (una pregunta tiene varias opciones con puntaje por área)
AREAS             1 ────< N OPCIONES            (cada opción pertenece a un área)
PREGUNTAS         1 ────< N OPCIONES_PREGUNTA   (opciones legacy del test original)
AREAS             1 ────< N RESULTADOS          (el resultado sugiere un área)
CARRERAS          1 ────< N GAME_CARRERAS       (una carrera puede aparecer en el juego)
CARRERAS          1 ────< N CARRERA_AREAS       (una carrera se asocia a varias áreas)
AREAS             1 ────< N CARRERA_AREAS       (un área agrupa varias carreras)
CARRERAS          M ────< N UNIVERSIDADES       (vía CARRERA_UNIVERSIDAD: qué universidad dicta cada carrera)
RESPUESTAS        N ────> 1 PREGUNTAS           (cada respuesta refiere a una pregunta)
RESPUESTAS        N ────> 1 OPCIONES            (cada respuesta selecciona una opción)
PASSWORD_RESETS   N ────> 1 USUARIOS            (códigos de recuperación por email del usuario)
USUARIOS          1 ────< 1 SESIONES_ACTIVAS    (una fila por usuario logueado con su última actividad)
```

### Cómo leer el diagrama

| Símbolo | Significado |
|---------|-------------|
| `\|\|--o{` | Uno a muchos (un registro en la tabla izquierda, varios en la derecha) |
| `\|\|--o\|` | Uno a uno opcional |
| `}o--o{` | Muchos a muchos |
| `PK` | Clave primaria (identificador único) |
| `FK` | Clave foránea (referencia a otra tabla) |
| `UK` | Clave única (no se puede repetir) |

---

## Referencia de tablas

### Tablas principales del sistema

#### `usuarios`
Usuarios del sistema (visitantes registrados, administradores y el dueño).

| Campo        |          Tipo           |  Clave  |                  Descripción                         |
|--------------|-------------------------|---------|------------------------------------------------------|
| `id`         | INT                     | PK      | Identificador único                                  |
| `nombre`     | VARCHAR(100)            |         | Nombre                                               |
| `apellido`   | VARCHAR(100)            |         | Apellido                                             |
| `email`      | VARCHAR(150)            | UNIQUE  | Correo electrónico (usado para login y recuperación) |
| `password`   | VARCHAR(255)            |         | Hash de la contraseña (Werkzeug)                     |
| `rol`        | ENUM('usuario','admin') |         | Rol de acceso                                        |
| `activo`     | TINYINT(1)              |         | 1 = habilitado, 0 = deshabilitado                    |
| `created_at` | DATETIME                |         | Fecha de alta                                        |
| `updated_at` | DATETIME                |         | Última actualización                                 |
| `es_dueño`   | TINYINT(1)              |         | 1 = dueño del panel (permisos exclusivos)            |

#### `tests`
Intentos de test vocacional realizados por los usuarios.

|        Campo        |     Tipo    |        Clave       |                 Descripción                      |
|---------------------|-------------|--------------------|--------------------------------------------------|
| `id`                | INT         | PK                 | Identificador                                    |
| `usuario_id`        | INT         | FK → `usuarios.id` | Usuario que realizó el test (borrado en cascada) |
| `fecha`             | DATETIME    |                    | Fecha del intento                                |
| `completado`        | TINYINT(1)  |                    | 1 = test finalizado                              |
| `fecha_realizacion` | TIMESTAMP   |                    | Fecha de realización                             |

#### `resultados`
Resultado del test: área vocacional sugerida y detalle.

|              Campo                |        Tipo         |          Clave           |            Descripción               |
|-----------------------------------|---------------------|--------------------------|--------------------------------------|
| `id`                              |        INT          | PK                       | Identificador                        |
| `test_id`                         |        INT          | FK → `tests.id` (UNIQUE) | Test asociado (1 resultado por test) |
| `area_profesional_sugerida`       |     VARCHAR(100)    |                          | Área recomendada                     |
| `area_id`                         |        INT          | FK → `areas.id`          | Área recomendada (relación formal)   |
| `puntaje`                         |        INT          |                          | Puntaje obtenido                     |
| `detalle`                         |     LONGTEXT        |                          | Detalle del resultado                |
| `created_at`                      |     DATETIME        |                          | Fecha de creación                    |
| `notas_personales`                |       TEXT          |                          | Notas editables por el usuario       |

### Tablas de preguntas y opciones

#### `preguntas`
Preguntas del test vocacional.

|        Campo       |      Tipo    | Clave |  Descripción  |
|--------------------|--------------|-------|---------------|
| `id`               | INT          | PK    | Identificador |
| `texto_pregunta`   | VARCHAR(255) |       | Enunciado     |
| `area_profesional` | VARCHAR(100) |       | Área asociada |

#### `opciones`
Opciones de respuesta con puntaje por área (esquema de puntuación actual).

|        Campo      |     Tipo     |        Clave        |           Descripción         |
|-------------------|--------------|---------------------|-------------------------------|
| `id`              | INT          | PK                  | Identificador                 |
| `pregunta_id`     | INT          | FK → `preguntas.id` | Pregunta (borrado en cascada) |
| `area_id`         | INT          | FK → `areas.id`     | Área a la que suma puntaje    |
| `texto`           | VARCHAR(255) |                     | Texto de la opción            |
| `puntaje`         | INT          |                     | Puntos que aporta             |

#### `opciones_pregunta`
Opciones del esquema original del test (legacy), conservadas por compatibilidad.

|        Campo       |     Tipo     |        Clave         |    Descripción     |
|--------------------|--------------|----------------------|--------------------|
| `id`               | INT          |  PK                  | Identificador      |
| `pregunta_id`      | INT          |  FK → `preguntas.id` | Pregunta           |
| `texto_opcion`     | VARCHAR(300) |                      | Texto de la opción |
| `area_profesional` | VARCHAR(100) |                      | Área               |

#### `respuestas`
Respuestas individuales de cada pregunta dentro de un test.

|     Campo     | Tipo |      Clave           |      Descripción      |
|---------------|------|----------------------|-----------------------|
| `id`          | INT  | PK                   | Identificador         |
| `test_id`     | INT  | FK → `tests.id`      | Test al que pertenece |
| `pregunta_id` | INT  | FK → `preguntas.id`  | Pregunta respondida   |
| `opcion_id`   | INT  | FK → `opciones.id`   | Opción elegida        |

### Tablas de áreas y categorías

#### `areas`
Áreas profesionales del test y de las carreras.

|     Campo     |    Tipo      | Clave |     Descripción      |
|---------------|--------------|-------|----------------------|
| `id`          | INT          |  PK   | Identificador        |
| `nombre`      | VARCHAR(100) |       | Nombre del área      |
| `descripcion` | TEXT         |       | Descripción          |
| `icono`       | VARCHAR(50)  |       | Ícono asociado       |
| `color`       | VARCHAR(20)  |       | Color representativo |

#### `orientaciones`
Orientaciones/áreas de agrupación de carreras gestionables desde el panel.

| Campo    |     Tipo     | Clave  |       Descripción        |
|----------|--------------|--------|--------------------------|
| `id`     | INT          | PK     | Identificador            |
| `nombre` | VARCHAR(100) | UNIQUE | Nombre de la orientación |

### Tablas de carreras

#### `carreras`
Catálogo de carreras de la plataforma.

|                      Campo                       |     Tipo     | Clave |                  Descripción                     |
|--------------------------------------------------|--------------|-------|--------------------------------------------------|
| `id`                                             | INT          |  PK   | Identificador                                    |
| `nombre`                                         | VARCHAR(150) |       | Nombre de la carrera                             |
| `descripcion`                                    | TEXT         |       | Descripción                                      |
| `area_profesional`                               | VARCHAR(100) |       | Área principal                                   |
| `instituciones`                                  | TEXT         |       | Instituciones donde se dicta                     |
| `popular`                                        | TINYINT(1)   |       | Marca si es popular                              |
| `imagen` / `imagen_portada` / `imagen_principal` | VARCHAR(500) |       | Rutas de imágenes (local o URL de Cloudinary)    |
| `video`                                          | VARCHAR(500) |       | Video de la carrera (URL, local o de Cloudinary) |
| `a_que_se_dedica`                                | TEXT         |       | Descripción del campo laboral                    |

#### `carrera_areas`
Tabla puente entre carreras y áreas.

|    Campo     |     Tipo     |        Clave       |  Descripción  |
|--------------|--------------|--------------------|---------------|
| `id`         | INT          | PK                 | Identificador |
| `carrera_id` | INT          | FK → `carreras.id` | Carrera       |  
| `area`       | VARCHAR(100) |                    | Área asociada |

### Tablas de universidades

#### `universidades`
Catálogo fijo de universidades de Tucumán con oferta en la plataforma. Se carga
por seed idempotente al arrancar (`core/migraciones.py`); las relaciones con
carreras se definen a mano tras verificar los sitios oficiales.

|    Campo     |           Tipo            |  Clave  |          Descripción               |
|--------------|---------------------------|---------|------------------------------------|
| `id`         | INT                       | PK      | Identificador                      |
| `nombre`     | VARCHAR(150)              | UNIQUE  | Nombre oficial de la institución   |
| `siglas`     | VARCHAR(20)               |         | Siglas de uso común (ej. `UNT`)    |
| `tipo`       | ENUM('publica','privada') |         | Gestión de la institución          |
| `sitio_web`  | VARCHAR(200)              |         | Dominio oficial (ej. `unt.edu.ar`) |
| `activo`     | TINYINT(1)                |         | 1 = visible en el sitio            |

#### `carrera_universidad`
Tabla puente entre carreras y universidades: qué universidad dicta cada carrera.

|      Campo       | Tipo |                Clave                  |        Descripción       |
|------------------|------|---------------------------------------|--------------------------|
| `carrera_id`     | INT  | PK, FK → `carreras.id` (CASCADE)      | Carrera                  |
| `universidad_id` | INT  | PK, FK → `universidades.id` (CASCADE) | Universidad que la dicta |

PK compuesta: un par carrera-universidad no puede repetirse. Ambas FKs usan
`ON DELETE CASCADE`. La columna `carreras.instituciones` (texto libre histórico)
quedó obsoleta: la fuente de verdad es ahora esta tabla.

### Tablas del juego

#### `game_carreras`
Configuración de las carreras que participan en el juego de descubrimiento.

|                  Campo                  |       Tipo      |        Clave        |       Descripción       |
|-----------------------------------------|-----------------|---------------------|-------------------------|
| `id`                                    | INT             | PK                  | Identificador           |
| `carrera_id`                            | INT             | FK → `carreras.id`  | Carrera                 |
| `texto_boton`                           | VARCHAR(100)    |                     | Texto del botón         |
| `titulo_card` / `descripcion_card`      | VARCHAR / T     |                     | Contenido de la tarjeta |
| `activo`                                | TINYINT(1)      |                     | Visible o no            |
| `orden`                                 | INT             |                     | Orden de aparición      |
| `boton_no` / `boton_info` / `boton_yes` | VARCHAR(100)    |                     | Textos de botones       |

#### `game_preguntas`
Preguntas del juego.

|                Campo                |     Tipo     | Clave |        Descripción         |
|-------------------------------------|--------------|-------|----------------------------|
| `id`                                | INT          | PK    | Identificador              |
| `texto_pregunta`                    | VARCHAR(300) |       | Enunciado                  |
| `opcion_a_texto` / `opcion_b_texto` | VARCHAR(200) |       | Textos de las dos opciones |
| `opcion_a_area` / `opcion_b_area`   | VARCHAR(100) |       | Áreas de cada opción       |
| `activo`                            | TINYINT(1)   |       | Visible o no               |
| `orden`                             | INT          |       | Orden                      |
| `fecha_creacion`                    | TIMESTAMP    |       | Fecha de alta              |

### Tablas de noticias

#### `noticias`
Noticias educativas mostradas en la sección de noticias.

|        Campo        |    Tipo      | Clave  |                 Descripción                      |
|---------------------|--------------|--------|--------------------------------------------------|
| `id`                | INT          | PK     | Identificador                                    |
| `titulo`            | VARCHAR(300) |        | Título                                           |
| `descripcion`       | TEXT         |        | Cuerpo/resumen                                   |
| `imagen`            | VARCHAR(500) |        | Imagen (ruta local o URL de Cloudinary)          |
| `video`             | VARCHAR(500) |        | Video de la noticia (URL, local o de Cloudinary) |
| `fuente`            | VARCHAR(100) |        | Fuente (nombre del medio)                        |
| `fecha`             | DATE         |        | Fecha de la noticia                              |
| `link`              | VARCHAR(500) | UNIQUE | Enlace de origen                                 |
| `categoria`         | VARCHAR(100) |        | Categoría                                        |
| `es_externa`        | TINYINT(1)   |        | 1 = redirige a link externo                      |
| `fecha_creacion`    | TIMESTAMP    |        | Fecha de alta                                    |

#### `fuentes`
Fuentes de noticias disponibles.

|   Campo   |    Tipo      |  Clave |     Descripción     |
|-----------|--------------|--------|---------------------|
| `id`      | INT          | PK     | Identificador       |
| `nombre`  | VARCHAR(100) | UNIQUE | Nombre de la fuente |
| `activo`  | TINYINT(1)   |        | Habilitada o no     |

#### `fuentes_eliminadas`
Registro de nombres de fuentes eliminadas (evita que una fuente dada de baja reingrese).

|   Campo   |     Tipo     | Clave |          Descripción          |
|-----------|--------------|-------|-------------------------------|
| `nombre`  | VARCHAR(100) |  PK   | Nombre de la fuente eliminada |

#### `filtros_fecha`
Filtros de tiempo ofrecidos al usuario en la sección de noticias.

|      Campo       |     Tipo     | Clave  |       Descripción         |
|------------------|--------------|--------|---------------------------|
| `id`             | INT          | PK     | Identificador             |
| `valor`          | VARCHAR(20)  | UNIQUE | Valor interno del filtro  |
| `etiqueta`       | VARCHAR(50)  |        | Texto visible             |
| `activo`         | TINYINT(1)   |        | Habilitado                |
| `orden`          | INT          |        | Orden de aparición        |
| `condicion`      | VARCHAR(250) |        | Condición SQL de filtrado |
| `es_fijo`        | TINYINT(1)   |        | No editable por el admin  |

### Tablas de soporte

#### `password_resets`
Códigos PIN de recuperación de contraseña.

|      Campo       |     Tipo     |             Clave               |      Descripción        |
|------------------|--------------|---------------------------------|-------------------------|
| `id`             | INT          | PK                              | Identificador           |
| `email`          | VARCHAR(255) | FK → `usuarios.email` (lógica)  | Email del usuario       |
| `codigo`         | VARCHAR(6)   | FK (lógica)                     | Código PIN de 6 dígitos |
| `usado`          | TINYINT(1)   |                                 | 1 = código ya utilizado |
| `expira_en`      | DATETIME     |                                 | Fecha de expiración     |
| `fecha_creacion` | TIMESTAMP    |                                 | Fecha de creación       |

#### `sesiones_activas`
Presencia en línea: una fila por usuario logueado con la última actividad registrada. Se actualiza en
cada request (como máximo 1 escritura por sesión cada 60 s) y las filas con más de 5 minutos sin
actividad se eliminan automáticamente. La tabla se crea sola al primer request; el dashboard la usa
para mostrar **"Usuarios en línea"** en tiempo real.

|   Campo     |           Tipo           |        Clave       |         Descripción            |
|-------------|--------------------------|--------------------|--------------------------------|
| `user_id`   | INT                      | PK → `usuarios.id` | Usuario con actividad reciente |
| `last_seen` | DATETIME                 |                    | Última fecha/hora de actividad |

---

## Relaciones entre entidades (resumen)

|     Origen    |      Cardinalidad     |       Destino       |                             Columna                             |
|---------------|-----------------------|---------------------|-----------------------------------------------------------------|
| `usuarios`    |    1 : N              | `tests`             | `tests.usuario_id`                                              |
| `tests`       |    1 : 1              | `resultados`        | `resultados.test_id`                                            |
| `tests`       |    1 : N              | `respuestas`        | `respuestas.test_id`                                            |
| `preguntas`   |    1 : N              | `opciones`          | `opciones.pregunta_id`                                          |
| `preguntas`   |    1 : N              | `opciones_pregunta` | `opciones_pregunta.pregunta_id`                                 |
| `areas`       |    1 : N              | `opciones`          | `opciones.area_id`                                              |
| `areas`       |    1 : N              | `resultados`        | `resultados.area_id`                                            |
| `respuestas`  |    N : 1              | `preguntas`         | `respuestas.pregunta_id`                                        |
| `respuestas`  |    N : 1              | `opciones`          | `respuestas.opcion_id`                                          |
| `carreras`    |    1 : N              | `game_carreras`     | `game_carreras.carrera_id`                                      |
| `carreras`    |    1 : N              | `carrera_areas`     | `carrera_areas.carrera_id`                                      |
| `carreras`    |    M : N (vía puente) | `universidades`     | `carrera_universidad` (`carrera_id`, `universidad_id`, CASCADE) |
| `usuarios`    |    1 : N              | `password_resets`   | `password_resets.email` (lógica)                                |
| `usuarios`    |    1 : 1              | `sesiones_activas`  | `sesiones_activas.user_id` (lógica, fila por usuario)           |

---

## Consideraciones de diseño

- **Claves primarias** definidas en todas las tablas (`id` autoincremental).

- **Claves foráneas** con `ON DELETE CASCADE` donde corresponde (tests → resultados, tests → respuestas,
  preguntas → opciones, preguntas → opciones_pregunta), garantizando integridad referencial.

- **Unicidad** en campos clave: `usuarios.email`, `noticias.link`, `fuentes.nombre`,
  `orientaciones.nombre`, `filtros_fecha.valor`, `resultados.test_id`, `sesiones_activas.user_id`.

- La tabla `sesiones_activas` no requiere dump: se crea automáticamente al primer request de un
  usuario logueado (`asegurar_tabla_sesiones_activas`).

- **Normalización**: el modelo está normalizado hasta la **3ª Forma Normal** (tablas de áreas y
  categorías separadas de las entidades que las usan; datos no repetidos; cada tabla depende de su PK).
  
- El esquema SQL completo se encuentra en `base de datos/futuro 360.sql`. Las
  migraciones históricas se aplican automáticamente al arrancar desde
  `core/migraciones.py` (`asegurar_columnas_esquema`, `asegurar_datos_iniciales`,
  `asegurar_tabla_game_carreras`, entre otras).