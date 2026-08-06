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
| Variables de entorno | python-dotenv |

## Estructura del proyecto

```
futuro 360/
├── app.py                       # Aplicación Flask: rutas y lógica del sitio y del panel
├── database_handler.py          # Conexión y ciclo de vida de la BD (una conexión por request)
├── requirements.txt             # Dependencias de Python
├── .env                         # Configuración local (NO se sube al repositorio)
├── .gitignore
├── base de datos/
│   ├── futuro 360.sql           # Esquema base + datos iniciales (carreras, preguntas, opciones)
│   ├── migracion_parte1.sql     # Migraciones históricas
│   └── migracion_parte2.sql
├── static/
│   ├── style.css                # Estilos del sitio público
│   ├── admin.css                # Estilos del panel admin
│   ├── img/                     # Fondos por tema y recursos gráficos
│   ├── imagenes/                # Imágenes del contenido
│   └── carreras/                # Imágenes de carreras
├── templates/                   # Plantillas Jinja2 del sitio y del panel
│   ├── index.html, login.html, registro.html, perfil.html
│   ├── test.html, resultado_detalle.html, mis_resultados.html
│   ├── carreras.html, carrera_detalle.html, juego.html, noticias.html
│   ├── recuperar_password.html, verificar_codigo.html, nueva_password.html
│   ├── dashboard.html, 404.html, base.html
│   └── admin/                   # Vistas del panel de administración
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

# 5. Importar la base de datos
#    (ejecutar el dump en el cliente MySQL o desde la app al primer inicio)
mysql -u root -p < "base de datos/futuro 360.sql"

# 6. Ejecutar la aplicación
python app.py
# El servidor queda disponible en http://localhost:5000
```

> **Nota**: al iniciar por primera vez, la aplicación sincroniza automáticamente los datos de imagen
> de las carreras y asegura la existencia de la cuenta del dueño del panel (ver sección *Panel de administración*).

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

# Cuenta del panel (dueño del sistema)
ADMIN_EMAIL=tu_correo@gmail.com
```

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DB_HOST` | No | Host del servidor MySQL (default `localhost`) |
| `DB_USER` | No | Usuario de MySQL (default `root`) |
| `DB_PASSWORD` | No | Contraseña de MySQL (default vacío) |
| `DB_NAME` | No | Nombre de la base de datos (default `futuro360`) |
| `SECRET_KEY` | Recomendada | Clave de firma de sesiones de Flask |
| `RESEND_API_KEY` | Solo para emails | Clave de la API de Resend |
| `ADMIN_EMAIL` | No | Email que identifica al **dueño** del panel (default `fabriciovillagra05@gmail.com`) |

**Importante:** el archivo `.env` no se sube al repositorio (está en `.gitignore`). No se debe
comprometer ninguna credencial en el código ni en los commits.

## Base de datos

- El esquema se encuentra en `base de datos/futuro 360.sql`.
- El modelo de datos completo (entidades, relaciones, claves) está documentado en
  [`docs/modelo_datos.md`](docs/modelo_datos.md).
- Las migraciones posteriores al dump base están en `base de datos/migracion_parte1.sql` y
  `migracion_parte2.sql`.

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
  principal envía los PIN directamente con Resend desde `app.py`.

## Autor

Fabricio Villagra — Tecnicatura Universitaria en Programación · UTN-FRT · Plan 2024
