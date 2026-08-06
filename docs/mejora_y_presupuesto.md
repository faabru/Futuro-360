# Mejora del Sistema y Presupuesto — Futuro 360

Documento correspondiente al criterio **"Mejora y Presupuesto del Sistema"** del TFI (CRITERIOS
PARA EL PROYECTO FINAL, pág. 19):

- Proponer una mejora concreta sobre el sistema original.
- Estimar las horas de trabajo necesarias.
- Definir un valor hora.
- Calcular el costo del sistema original.
- Calcular el costo de la ampliación.
- Presentar el presupuesto total del sistema con la mejora.

---

## 1. Mejora concreta propuesta

### Nombre
**Módulo de Estadísticas con Informes PDF** (panel administrativo + resultado del estudiante).

### Alcance
La mejora agrega dos funcionalidades nuevas al sistema existente:

1. **Dashboard de estadísticas con gráficos** en el panel de administración (`/admin`):
   - Cantidad de usuarios registrados y usuarios activos.
   - Distribución de usuarios por **área profesional sugerida** (gráfico de torta/donut).
   - Cantidad de **tests realizados** y evolución en el tiempo (gráfico de líneas/barras).
   - **Ranking de carreras** más consultadas.
   - Cantidad de noticias por fuente y por categoría.
   - Accesible solo para administradores (rol `admin` / dueño).

2. **Informe PDF del resultado vocacional** para el estudiante:
   - Botón "Descargar informe PDF" en la pantalla de detalle del resultado.
   - El PDF incluye: datos del estudiante, área sugerida, puntaje obtenido, detalle del área,
     lista de carreras recomendadas y notas personales.
   - Formato profesional (encabezado, colores de la marca, tabla de puntajes).

### Justificación y beneficios
- **Completa la funcionalidad de reportes** del sistema: ya existía la exportación **Excel** de
  datos administrativos (requisito excluyente cumplido) y esta mejora agrega **reportes en PDF**
  orientados al usuario final y **visualización de información en pantalla** (gráficos).
- **Valor para el estudiante**: recibir un informe descargable y presentable de su orientación
  vocacional mejora la experiencia y la utilidad real de la plataforma.
- **Valor para el administrador**: monitoreo visual de la actividad y de la efectividad del
  contenido, útil para la toma de decisiones (qué carreras difundir, qué áreas tienen más demanda).
- **Integra conocimientos de la carrera**: generación de documentos (PDF), librerías de
  visualización de datos (Chart.js), consultas agregadas SQL (GROUP BY, funciones de agregación)
  y nuevas vistas del panel.

### Enfoque técnico
| Componente | Tecnología propuesta |
|---|---|
| Gráficos del dashboard | Chart.js (CDN) + datos JSON servidos desde Flask |
| Informe PDF | ReportLab (generación server-side en Python) |
| Consultas de estadísticas | SQL agregado sobre las tablas existentes (`usuarios`, `tests`, `resultados`, `noticias`, `carreras`) |
| Autorización | Decoradores existentes `requiere_admin` |
| Datos | Sin cambios de esquema: se reutilizan tablas actuales |

### Verificación de aceptación
- `/admin` muestra al menos 4 gráficos/indicadores con datos reales.
- El informe PDF se genera y descarga correctamente desde el detalle del resultado.
- Los datos de los gráficos se actualizan al cambiar la información en la base.
- El acceso a la estadística requiere sesión de administrador.

---

## 2. Estimación de horas

### 2.1 Estimación del sistema original (sin la mejora)

| # | Tarea | Horas |
|---|---|---|
| 1 | Relevamiento de requisitos y diseño del modelo de datos | 12 |
| 2 | Configuración de la arquitectura (Flask + MySQL + entorno) | 8 |
| 3 | Registro, login, roles y recuperación de contraseña | 20 |
| 4 | Test vocacional (preguntas, opciones, puntaje, resultados) | 25 |
| 5 | Catálogo de carreras, detalle y búsqueda de universidades | 18 |
| 6 | Juego interactivo de descubrimiento | 15 |
| 7 | Módulo de noticias (fuentes, filtros de fecha) | 12 |
| 8 | Panel de administración (ABM usuarios, carreras, preguntas, noticias, juego) | 35 |
| 9 | Exportación de datos a Excel | 10 |
| 10 | Diseño de interfaz, responsive y temas (claro/oscuro) | 15 |
| 11 | Pruebas y correcciones | 15 |
| 12 | Documentación técnica y despliegue | 10 |
| | **TOTAL SISTEMA ORIGINAL** | **195 hs** |

### 2.2 Estimación de la ampliación (la mejora)

| # | Tarea | Horas |
|---|---|---|
| 1 | Análisis y diseño de la mejora | 4 |
| 2 | Dashboard de estadísticas con gráficos (Chart.js + consultas SQL) | 18 |
| 3 | Generación del informe PDF del resultado (ReportLab) | 12 |
| 4 | Ajustes de interfaz, pruebas y correcciones | 6 |
| | **TOTAL AMPLIACIÓN** | **40 hs** |

---

## 3. Valor hora

Valor hora definido para el desarrollo: **$ 15.000 ARS / hora**
(desarrollador freelance nivel inicial, mercado Tucumán/Argentina. Este valor es un parámetro
ajustable por el estudiante según su contexto).

---

## 4. Cálculo de costos

| Concepto | Horas | Valor hora | Costo |
|---|---|---|---|
| Costo del sistema original | 195 | $ 15.000 | **$ 2.925.000** |
| Costo de la ampliación (mejora) | 40 | $ 15.000 | **$ 600.000** |
| **Presupuesto total (sistema + mejora)** | 235 | $ 15.000 | **$ 3.525.000** |

### Fórmulas utilizadas

```
Costo original    = 195 hs × $ 15.000 = $ 2.925.000
Costo ampliación  =  40 hs × $ 15.000 = $   600.000
Presupuesto total = $ 2.925.000 + $ 600.000 = $ 3.525.000
```

Si se desea recalcular con otro valor hora `V`, el presupuesto total es: **235 hs × V**.

---

## 5. Resumen

- **Mejora propuesta**: Módulo de estadísticas con informes PDF (dashboard con gráficos para el
  admin + informe PDF del resultado para el estudiante).
- **Horas de la mejora**: 40 hs.
- **Costo de la mejora**: $ 600.000 ARS.
- **Costo del sistema original**: $ 2.925.000 ARS.
- **Presupuesto total con la mejora**: **$ 3.525.000 ARS**.
