
# Manual de Usuario — Futuro 360

Plataforma de orientación vocacional para estudiantes de Tucumán. Este manual explica el uso del
**sitio público** (para cualquier visitante o usuario registrado) y del **panel de administración**
(para el personal que gestiona el contenido).

---

## SITIO PÚBLICO - (para todos los usuarios)

### 1. Acceso a tu cuenta

#### 1.1 Registro de cuenta

1. Entrar a la página principal y hacer clic en **Registrarse**.
2. Completar **nombre**, **apellido**, **email** y **contraseña**.
3. Enviar el formulario. La cuenta queda creada como **usuario** estándar.

> El email debe ser único. Si ya existe una cuenta con ese correo, el sistema lo informa.

#### 1.2 Iniciar sesión

1. Hacer clic en **Iniciar sesión**.
2. Ingresar **email** y **contraseña**.
3. El sistema valida las credenciales y redirige al **dashboard** del usuario.

#### 1.3 Recuperación de contraseña

Si el usuario olvida su contraseña:

1. En la página de login, hacer clic en **¿Olvidaste tu contraseña?**.
2. Ingresar el email de la cuenta.
3. El sistema envía un **código PIN de 6 dígitos** al correo (revisar también la carpeta de spam).
4. Ingresar el código en la pantalla de verificación.
5. Definir una **nueva contraseña** y confirmarla.

> El código expira en 15 minutos. Por seguridad, el sistema muestra el mismo mensaje de éxito
> aunque el email no exista, para no revelar qué cuentas están registradas.

#### 1.4 Perfil

Desde **Mi perfil**, el usuario puede:
- Ver y editar sus datos personales (nombre, apellido, email).
- Cambiar su contraseña.
- Eliminar su cuenta (baja de usuario).

### 2. Herramientas de orientación vocacional---(DASHBOARD)

#### 2.1 Test vocacional

Es la funcionalidad principal de la plataforma:

1. Entrar a la sección **Test vocacional**.
2. Responder las **29 preguntas** eligiendo la opción que mejor describa sus intereses.
3. Al finalizar, el sistema calcula el **área profesional** más afín según el puntaje acumulado.
4. El resultado se guarda y muestra las **carreras recomendadas** dentro de esa área.

#### 2.2 Mis resultados

- La sección **Mis resultados** lista todos los tests realizados por el usuario.
- Al abrir un resultado se puede ver el **área sugerida**, el detalle y las **notas personales**.
- Las notas personales se pueden **editar** desde la misma pantalla.

#### 2.3 Explorar carreras

- La sección **Carreras** muestra todas las carreras ordenadas por área profesional.
- Cada carrera tiene: **nombre**, **descripción** y **área**; dónde se dicta se consulta con los buscadores de universidades.
- Se pueden filtrar o buscar por área de interés.
- En el detalle de cada carrera, la sección **"¿Dónde estudiarla en Tucumán?"** ofrece dos buscadores:
  - **"Buscar universidades"**: realiza una búsqueda en **DuckDuckGo** sobre las universidades
    **verificadas que dictan la carrera en Tucumán** y trae los links de sus sitios oficiales.
  - **"Búsqueda personalizada"**: abre **Google** con la carrera ya escrita para afinar la búsqueda.
- Los resultados de DuckDuckGo se muestran dentro de la página (título, enlace y descripción);
  si la búsqueda automática falla, se ofrece un enlace directo a DuckDuckGo.

#### 2.4 Juego de descubrimiento

- La sección **Juego** ofrece dos experiencias: **"Descubrí Tu Carrera"** (tarjetas de carreras con
  los botones **"Me interesa"**, **"No es lo mío"** e **"Info"**) e **"Intereses en Juego"**
  (escenarios con dos opciones de respuesta).
- Solo aparecen las carreras y preguntas marcadas como **activas** desde el panel.
- Al final de cada partida hay un botón **"Jugar de nuevo"** que reinicia el juego desde el inicio
  sin recargar la página.

### 3. Contenido del sitio

#### 3.1 Noticias

- La sección **Noticias** muestra novedades educativas de la región.
- Las noticias provienen de **fuentes** configuradas por el administrador y se agrupan por
  **categoría** y **filtro de fecha** (por ejemplo: semana, mes, año).
- Cada noticia puede abrirse en su **link de origen** si es externa.

#### 3.2 Contacto / comentarios

- La sección de **comentarios** permite a los visitantes dejar un mensaje de contacto con nombre,
  email y texto.

---

## PANEL DE ADMINISTRACIÓn - (para administradores)

El panel se accede desde **`/admin`** en el navegador. Se ingresa **solo con email y contraseña**
de una cuenta con rol `admin` activa.

### 1. Acceso y roles

#### 1.1 Roles

|            Rol             |                                Descripción                                |
|----------------------------|---------------------------------------------------------------------------|
| **Usuario**                | Acceso solo al sitio público.                                             |
| **Administrador**          | Acceso completo al panel.                                                 |
| **Dueño**                  | Administrador con permisos exclusivos (gestión de otros administradores). |

El **dueño** puede:
- Editar o eliminar a **otros administradores**.
- Desactivar cuentas de administradores.

El **dueño no puede** (la cuenta está protegida):
- Eliminarse a sí mismo.
- Desactivar su propia cuenta.
- Editarse a sí mismo desde el panel.

#### 1.2 Dashboard

Pantalla inicial del panel con el resumen de la actividad del sistema. Muestra tarjetas (KPI) con:

- **Usuarios**, **Carreras**, **Preguntas del test**, **Noticias** y **Noticias de hoy**.
- **Juego (Car/Preg)**: carreras y preguntas activas en el mini-juego.
- **Usuarios en línea**: cantidad de usuarios **conectados ahora mismo** (usuarios con actividad en
  los últimos 5 minutos). Se refresca sola cada 30 segundos, sin recargar la página. Para que un
  usuario aparezca/e desaparezca basta con que navegue o cierre el sitio; pasados 5 minutos sin
  actividad deja de contarse.
- **Tests realizados**: cuenta **todos** los tests de **todos** los usuarios (si un usuario hizo
  varios tests, cada uno suma), e indica cuántos usuarios distintos los realizaron.

Debajo se presentan los **gráficos** (usuarios por área sugerida, tests por mes, noticias por fuente
y por categoría) y el listado de usuarios. También es la puerta de entrada a todas las secciones de
gestión del panel.

### 2. Gestión de contenido

#### 2.1 Carreras

Desde **Carreras** se gestiona el catálogo de carreras:

- Listado con búsqueda/filtro.
- **Alta** de carrera: nombre, descripción, área profesional e instituciones.
- **Edición** de carrera: todos sus datos e **imágenes** (portada/principal) y **video** opcional.
- **Baja** de carrera.
- **Exportar Excel** de la lista de carreras.

**Imágenes y video:** en el alta/edición se puede **subir un archivo** desde el
dispositivo o **pegar una URL** (por ejemplo de Cloudinary). Si la aplicación
tiene Cloudinary configurado, los archivos subidos se guardan en la nube; si no,
se guardan localmente. Ante cualquier problema de subida, la carrera se guarda
igual con el archivo local.

#### 2.2 Orientaciones

Sección para gestionar las **áreas/orientaciones profesionales** que agrupan las carreras
(por ejemplo: Tecnología, Salud, Ingeniería, Negocios, etc.). Permite **crear** y **eliminar**
orientaciones.

#### 2.3 Preguntas y opciones del test

Desde **Preguntas** se administra el contenido del test vocacional:

- **Alta** de pregunta: texto y área profesional.
- **Alta de opciones** para cada pregunta: texto y área que suma puntaje.
- **Baja** de preguntas y de opciones individuales.
- **Exportar Excel** de preguntas y opciones.

#### 2.4 Juego

- **Carreras del juego**: configurar qué carreras participan en la sección Juego, con textos de
  botones, título y descripción de tarjeta, orden y estado activo.
- **Preguntas del juego**: alta, edición, activar/desactivar y baja de las preguntas del juego.
- Ambas pantallas muestran tarjetas con **Total / Activas / Inactivas**. Al activar o desactivar una
  carrera o pregunta, el botón y los contadores se actualizan **al instante** (AJAX), sin recargar.

### 3. Gestión de noticias

#### 3.1 Fuentes

Alta, edición, activar/desactivar y baja de las fuentes de noticias (por ejemplo: nombre del
medio/portal).

#### 3.2 Filtros de fecha

Alta, edición, orden y baja de los filtros de tiempo que se ofrecen al usuario final
(ej: "Hoy", "Esta semana", "Este mes").

#### 3.3 Noticias

Alta, edición y baja de noticias (título, descripción, imagen, **video** opcional, fuente, fecha,
categoría, link). Incluye **Exportar Excel** de la lista de noticias.

Al igual que las carreras, cada noticia admite una **imagen** y un **video**:
subirlos desde el dispositivo o pegar una URL. Si Cloudinary está configurado,
quedan en la nube (URL pública); si no, localmente.

### 4. Gestión de usuarios

Desde **Usuarios** se realiza el ABM completo (Alta, Baja, Modificación y Consulta):

- **Listado**: tabla con nombre, email, rol y estado. Incluye indicador **DUEÑO** cuando corresponde.
- **Alta**: formulario para crear un nuevo usuario (nombre, apellido, email, contraseña, rol, estado).
- **Modificación**: editar datos de un usuario (nombre, apellido, email, contraseña, rol).
- **Baja**: eliminar un usuario de la base.
- **Activar / Desactivar**: conmutar el estado `activo` de una cuenta. Un usuario desactivado no
  puede iniciar sesión.
- **Exportar Excel**: genera un archivo `.xlsx` con la lista completa de usuarios.

### 5. Herramientas del admin

#### 5.1 Exportación de reportes (Excel)

Requisito excluyente del TFI: exportación de datos.

Cada sección habilitada muestra un botón **"Exportar Excel"** que descarga un archivo `.xlsx`
con formato profesional:

- Encabezados con fondo oscuro y texto blanco.
- Filas alternadas para facilitar la lectura.
- **Autofiltro** en los encabezados.
- **Panel congelado** (encabezado fijo al desplazarse).
- Hoja **Resumen** con la fecha de exportación y el total de registros.

#### 5.2 Recuperación de contraseña del panel

El panel cuenta con su propio flujo de recuperación de contraseña (paso por paso: email → PIN →
nueva contraseña), equivalente al del sitio público.

---

## PREGUNTAS FRECUENTES

### Sitio público

**¿Cómo recupero mi contraseña si no llega el código?**
Revisar la carpeta de spam y esperar unos minutos. El código expira a los 15 minutos de solicitado.

### Panel de administración

**¿Por qué un administrador no puede eliminar a otro administrador?**
Por seguridad, esa acción es exclusiva del **dueño** del sistema.

**¿Qué pasa si desactivo mi propia cuenta de administrador?**
No es posible: el sistema bloquea la auto-desactivación y la auto-eliminación para evitar dejar el
panel sin administración.

**¿El exportado a Excel funciona en cualquier navegador?**
Sí: el archivo `.xlsx` se genera en el servidor y se descarga por el navegador sin necesidad de
complementos.

**¿Cómo se guardan las imágenes y videos que subo al panel?**
Depende de la configuración: si se definieron las claves de **Cloudinary** en el `.env`, se suben a
la nube y quedan accesibles por URL (se comparten entre máquinas). Sin las claves, o si Cloudinary
falla, se guardan en `static/imagenes/` localmente. El sistema nunca deja de funcionar por esto.