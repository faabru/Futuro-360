# Futuro 360 — Orientación Vocacional

**Trabajo Final Integrador (TFI)** · Tecnicatura Universitaria en Programación · UTN-FRT · Plan 2024

Plataforma web de orientación vocacional para estudiantes de la provincia de Tucumán, Argentina. Permite descubrir carreras según los intereses de cada persona mediante un **test vocacional**, explorar **carreras y universidades**, consultar **noticias educativas**, jugar a un **juego de descubrimiento** y gestionar todo el contenido desde un **panel de administración**.

## Características principales

### Sitio público
- **Test vocacional** de 30 preguntas con puntaje por área profesional y recomendación de carreras.
- **Informe PDF** descargable del resultado vocacional (área dominante, afinidad por área y carreras recomendadas).
- **Exploración de carreras** (40+ carreras) por área profesional, con detalle, descripción e instituciones.
- **Búsqueda de universidades** por carrera.
- **Juego interactivo** de descubrimiento de carreras.
- **Noticias educativas** con fuentes, categorías y filtros por fecha.
- **Registro / Login / Perfil** de usuarios.
- **Recuperación de contraseña** por código PIN enviado por email (Resend).
- **Historial de resultados** del test para cada usuario.
- **Sección de comentarios / contacto**.

### Panel de administración (`/admin`)
- ABM completo de **usuarios** (alta, baja, modificación, activar/desactivar, roles).
- ABM de **carreras**, **orientaciones**, **preguntas y opciones** del test.
- Gestión del **juego** (carreras y preguntas).
- Gestión de **noticias**, **fuentes** y **filtros de fecha**.
- **Estadísticas con gráficos** (usuarios por área sugerida, tests por mes, noticias por fuente y categoría).
- **Exportación a Excel (.xlsx)** de usuarios, carreras, preguntas y noticias.
- **Roles diferenciados**: Administrador y Usuario, más un rol especial **Dueño** con permisos exclusivos.

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3 + Flask 3 |
| Base de datos | MySQL (conector `mysql-connector-python`) |
| Frontend | HTML + CSS + JavaScript (plantillas Jinja2) |
| Envío de emails | Resend |
| Exportación Excel | openpyxl |
| Informe PDF | reportlab |
| Media (imágenes y videos) | Cloudinary (con fallback local) |
| Variables de entorno | python-dotenv |

## Estructura del proyecto

La aplicación está organizada siguiendo el patrón de **blueprints de Flask**: cada
funcionalidad vive en su propio módulo y la entrada principal queda reducida a una
fábrica (`create_app`) que registra todos los módulos.

```
futuro 360/
├── app.py                       # Punto de entrada: fábrica create_app() + arranque del servidor
├── config.py                    # Configuración central (BD, seguridad, email, constantes)
├── database_handler.py          # Conexión y ciclo de vida de la BD (una conexión por request)
├── core/                        # Lógica transversal reutilizable
│   ├── decoradores.py           # requiere_login, requiere_admin, ajax_o_redirect, es_usuario_dueño
│   ├── imagenes.py              # Subida de imágenes/videos (Cloudinary con fallback local)
│   ├── migraciones.py           # Auto-migraciones idempotentes (tablas, columnas, datos iniciales)
│   ├── mailer.py                # Envío de emails con Resend (códigos de recuperación)
│   └── startup.py               # Sincronización de imágenes al arrancar
├── blueprints/
│   ├── sitio/                   # Rutas del sitio público
│   │   ├── auth.py              # Registro, login, logout, recuperación de contraseña, perfil
│   │   ├── principal.py         # Portada, dashboard del usuario, comentarios
│   │   ├── vocacional.py        # Test vocacional, resultados e informe PDF
│   │   ├── carreras.py          # Catálogo de carreras y búsqueda de universidades
│   │   ├── juegos.py            # Mini-juego de descubrimiento de carreras
│   │   └── noticias.py          # Sección de noticias
│   └── admin/                   # Rutas del panel de administración
│       ├── auth.py              # Login, logout y recuperación de contraseña del panel
│       ├── dashboard.py         # Pantalla principal (estadísticas y gráficos)
│       ├── usuarios.py          # ABM completo de usuarios
│       ├── orientaciones.py     # Áreas/orientaciones profesionales
│       ├── carreras.py          # ABM de carreras
│       ├── preguntas.py         # ABM de preguntas y opciones del test
│       ├── juego.py             # ABM de carreras y preguntas del juego
│       ├── reportes.py          # Exportación de datos a Excel
│       └── noticias.py          # ABM de noticias, fuentes y filtros de fecha
├── scripts/                     # Utilidades de desarrollo (sync de imágenes, checks, etc.)
├── requirements.txt             # Dependencias de Python
├── .env                         # Configuración local (NO se sube al repositorio)
├── .gitignore
├── base de datos/
│   └── futuro 360.sql           # Esquema base + datos iniciales (carreras, preguntas, opciones)
├── static/
│   ├── style.css                # Estilos del sitio público
│   ├── admin.css                # Estilos del panel admin
│   ├── img/                     # Fondos por tema y recursos gráficos
│   ├── imagenes/                # Imágenes del contenido
│   └── carreras/                # Imágenes de carreras
├── templates/                   # Plantillas Jinja2 del sitio y del panel
|   |
│   ├── index.html, login.html, registro.html, perfil.html
│   ├── test.html, resultado_detalle.html, mis_resultados.html
│   ├── carreras.html, carrera_detalle.html, juego.html, noticias.html
│   ├── recuperar_password.html, verificar_codigo.html, nueva_password.html
│   ├── dashboard.html, 404.html, 500.html, base.html
│   └── admin/                   # Vistas del panel de administración
|
├── recuperacion de contraseña/  # Servicio Node.js (alternativa) de envío de PIN
├── README.md
└── docs/
    ├── manual_usuario.md        # Manual de usuario
    └── modelo_datos.md          # Modelo entidad/relación de la base de datos
```

## Requisitos previos

- Python 3.10 o superior
- MySQL 5.7 / 8.x (servidor local o remoto)
- `pip` y `venv` disponibles
- (Opcional) Cuenta en [Resend](https://resend.com) para el envío de emails

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/faabru/Futuro-360.git
cd "futuro 360"

# 2. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el archivo de configuración .env (ver sección siguiente)

# 5. Ejecutar la aplicación (¡no hace falta importar nada!)
python app.py
# En el primer arranque la app crea la base `futuro360` (si no existe),
# sus tablas y siembra el contenido de referencia (carreras, noticias,
# fuentes, preguntas del juego, etc.) automáticamente.
# El servidor queda disponible en http://localhost:5000
```

> **Nota**: si preferís importar el dump a mano, seguí usando
> `base de datos/futuro 360.sql`. Es opcional: al arrancar, la aplicación
> crea la base, las tablas y el contenido si faltan, y **nunca pisa datos
> que ya existan** (solo completa tablas vacías).

## Configuración (archivo `.env`)

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=futuro360

# Seguridad
SECRET_KEY=una_cadena_larga_y_aleatoria

# Envío de emails (Resend)
RESEND_API_KEY=re_XXXXXXXXXXXXX

# Cuenta del panel (dueño del sistema, POR MÁQUINA)
# Cada persona pone su propio correo y su propia contraseña inicial.
# Esa cuenta se crea en SU base al primer arranque.
ADMIN_EMAIL=tu_correo@gmail.com
ADMIN_PASSWORD=tu_contraseña_inicial

# Imágenes y videos (Cloudinary) — OPCIONAL
# Sin estas claves la app guarda los archivos localmente (igual funciona).
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DB_HOST` | No | Host del servidor MySQL (default `localhost`) |
| `DB_USER` | No | Usuario de MySQL (default `root`) |
| `DB_PASSWORD` | No | Contraseña de MySQL (default vacío) |
| `DB_NAME` | No | Nombre de la base de datos (default `futuro360`) |
| `SECRET_KEY` | Recomendada | Clave de firma de sesiones de Flask |
| `RESEND_API_KEY` | Solo para emails | Clave de la API de Resend |
| `CLOUDINARY_CLOUD_NAME` | No | Cloud de Cloudinary para imágenes/videos |
| `CLOUDINARY_API_KEY` | No | API key de Cloudinary |
| `CLOUDINARY_API_SECRET` | No | API secret de Cloudinary |
| `ADMIN_EMAIL` | No | Email del **dueño del panel** en esta máquina (default `fabriciovillagra05@gmail.com`) |
| `ADMIN_PASSWORD` | No | Contraseña SOLO para crear esa cuenta la primera vez (default `123456789`). Luego puede cambiarse con la recuperación. |

**Importante:** el archivo `.env` no se sube al repositorio (está en `.gitignore`). No se debe
comprometer ninguna credencial en el código ni en los commits.

## Base de datos

La base se prepara **sola al primer arranque** (no hace falta importar nada):

- Al iniciar, la aplicación **crea la base `futuro360` si no existe**, crea las
  tablas que falten y **siembra el contenido de referencia** (carreras,
  noticias, fuentes, preguntas del juego, orientaciones) usando como fuente
  `base de datos/futuro 360.sql`.
- Solo completa tablas **vacías** (o crea las que no existan): nunca pisa
  registros que ya haya en la máquina.
- **Las cuentas de usuario NO viajan en el contenido**: cada máquina crea la
  suya. La cuenta del dueño/admin se crea al primer arranque con tu
  `ADMIN_EMAIL` y `ADMIN_PASSWORD` del `.env`, y las demás se registran desde
  el sitio. Así vos entras con tu correo/contraseña y tu compañera con los suyos.
- El dump `base de datos/futuro 360.sql` también puede importarse a mano
  (MySQL Workbench → Open SQL Script), pero es opcional con el auto-arranque.
- El dump se regenera con `python scripts/exportar_base.py` cada vez que quieras
  publicar contenido nuevo para los demás (no editar el archivo a mano).
- **Para compartir contenido entre máquinas**: corré
  `python scripts/exportar_base.py`, subí el archivo regenerado a GitHub, y la
  otra persona solo hace `git pull` y arranca la app: la toma sola.
- El modelo de datos completo (entidades, relaciones, claves) está documentado en
  [`docs/modelo_datos.md`](docs/modelo_datos.md).
- Las migraciones históricas ya no son manuales: las columnas nuevas (p. ej. `popular`)
  y los datos iniciales (opción "Ninguna de las anteriores") se aseguran
  automáticamente al arrancar desde `core/migraciones.py`.

## Imágenes y videos (Cloudinary)

Las **imágenes y videos** de carreras y noticias se suben a
[Cloudinary](https://cloudinary.com) (plan gratuito, 25 GB). Así los archivos
viven en la nube, se comparten entre máquinas y no ocupan espacio en el repo.

### Cómo funciona

- `core/imagenes.py` centraliza las subidas (`guardar_archivo`).
- Si Cloudinary está configurado (las tres variables en el `.env`), el archivo
  se sube a la nube y se guarda su **URL pública** en la base de datos.
- Si **no** está configurado, o Cloudinary falla por cualquier motivo
  (credenciales, permisos, red), la app **sigue funcionando**: guarda el
  archivo localmente en `static/imagenes/` y no rompe el panel.
- En las plantillas, el filtro Jinja `|media` (registrado en `app.py`) resuelve
  cada valor: las rutas locales (`imagenes/...`) las convierte a
  `/static/imagenes/...` y las URLs completas (`https://res.cloudinary.com/...`)
  las deja tal cual.
- En el alta/edición de una carrera o noticia se puede **pegar la URL** de un
  medio o **subir un archivo** desde el dispositivo (imagen, y opcionalmente
  video: mp4, webm, mov, avi, mkv, m4v).

### Activar Cloudinary

1. Crear la cuenta en [cloudinary.com](https://cloudinary.com). El **cloud name**
   figura en Settings → API Keys (es el mismo del "Entorno del producto").
2. Completar en el `.env`:

```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

3. Reiniciar la app. La **primera subida** en el panel carrea el resto.

> **Importante — rol de la API key:** la key debe tener rol **Master Admin**.
> Si se crea con el rol "Media Library User", la app firma bien pero Cloudinary
> rechaza la subida con
> `Request forbidden due to missing permissions (actions=["create"])`.
> Se corrige en Cloudinary → Settings → **API Keys** → editar la key → rol
> **Master Admin**.

> **Importante — copiar el API Secret:** el secreto se copia con el **botón de
> copiar** de Cloudinary (Settings → API Keys → columna "API secret"). No se
> debe escribir a mano: es largo y con caracteres mixtos; cualquier carácter de
> más o de menos produce `Invalid Signature`. La API key y su secret deben ser
> **del mismo par** (mezclarlos con otra key da exactamente ese error).

### Migrar imágenes existentes

Para mover a la nube las imágenes que ya están guardadas localmente
(`static/imagenes/`) — migración única:

```bash
python scripts/migrar_imagenes_cloudinary.py
```

Sube `imagen`, `imagen_portada` e `imagen_principal` de carreras y `imagen` de
noticias (solo las que empiezan con `imagenes/`) y actualiza la base de datos.
Si Cloudinary no está configurado, avisa y no hace nada.

### Solución de problemas

| Error de Cloudinary | Causa | Solución |
|---|---|---|
| `Invalid Signature` | API key y API secret no son del mismo par, o el secret quedó incompleto al escribirse a mano | Revisar que la key use el secret correcto (copiar con el botón de copiar) en Settings → API Keys |
| `Request forbidden due to missing permissions (actions=["create"])` | La API key tiene rol "Media Library User" que no permite subir | Cambiar el rol de la key a **Master Admin** |
| `Invalid image file` | El archivo no es una imagen/video válido | El panel valida extensiones; verificar que el archivo no esté corrupto |

## Panel de administración

- URL: `http://localhost:5000/admin`
- El acceso al panel se realiza **solo por email** contra la tabla `usuarios` (rol `admin` y `activo = 1`).
- La cuenta definida en `ADMIN_EMAIL` se crea automáticamente al primer inicio con rol **administrador dueño**
  (columna `es_dueño`). Si ya existía con otra contraseña, se conserva la contraseña conocida.
- **Dueño** vs. **Administrador**:

| Capacidad | Administrador | Dueño |
|---|---|---|
| ABM de usuarios | Sí | Sí |
| Editar/eliminar otros administradores | No | Sí |
| Editar/eliminar la propia cuenta del dueño | No | No (protegida) |
| Resto del panel (carreras, noticias, juego, exportación) | Sí | Sí |

## Exportación de reportes

Desde el panel, los botones **"Exportar Excel"** generan archivos `.xlsx` con:
- Lista de **usuarios**
- Lista de **carreras**
- Preguntas y opciones del **test**
- **Noticias**

Los archivos incluyen encabezados con estilo, filas alternadas, autofiltro, panel congelado y una
hoja de resumen. Este cumplimiento de **exportación de datos** (PDF, Excel o CSV) es requisito
excluyente del TFI.

## Documentación

- [`docs/manual_usuario.md`](docs/manual_usuario.md) — guía de uso del sitio y del panel admin.
- [`docs/modelo_datos.md`](docs/modelo_datos.md) — diagrama entidad/relación y referencia de tablas.
- [`docs/mejora_y_presupuesto.md`](docs/mejora_y_presupuesto.md) — mejora propuesta, estimación de horas y presupuesto del sistema (criterio TFI).

## Notas de despliegue (producción)

- Para producción se recomienda un servidor WSGI (por ejemplo `waitress` o `gunicorn` en Linux)
  en lugar de `app.run(debug=True)`.
- Configurar `SECRET_KEY` y las credenciales de BD en el entorno de producción.
- La base de datos `futuro360` debe estar creada e importada antes de iniciar.
- El servicio Node de `recuperacion de contraseña/` es un módulo alternativo opcional; la aplicación
  principal envía los PIN directamente con Resend desde `core/mailer.py`.

## Autor

Fabricio Villagra — Tecnicatura Universitaria en Programación · UTN-FRT · Plan 2024
