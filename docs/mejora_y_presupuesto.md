# Mejora del Sistema y Presupuesto — Futuro 360

Documento correspondiente al criterio **"Mejora y Presupuesto del Sistema"** del TFI (CRITERIOS
PARA EL PROYECTO FINAL, pág. 19):

- Proponer una mejora concreta sobre el sistema original.
- Estimar las horas de trabajo necesarias.
- Definir un valor hora.
- Calcular el costo del sistema original.
- Calcular el costo de la ampliación.
- Presentar el presupuesto total del sistema con la mejora.

> **Nota:** la mejora anterior de este documento (dashboard de estadísticas + informe PDF) ya
> está implementada en el sistema. Esta versión propone una **nueva mejora**: un recomendador
> de carreras basado en Machine Learning, que reemplaza al presupuesto anterior como mejora
> propuesta a estimar y presupuestar.

---

## 1. Mejora concreta propuesta

### Nombre
**Recomendador Inteligente de Carreras (Machine Learning)**

### Situación actual
Hoy el test vocacional calcula el resultado con un **puntaje acumulado por área** (suma simple de
respuestas): el área con más puntos define la recomendación de carreras. Es un enfoque basado en
reglas fijas, sin aprendizaje ni ajuste a partir del comportamiento real de los usuarios.

### Alcance
La mejora incorpora un modelo de **aprendizaje automático** que complementa (no reemplaza) el
puntaje actual, entrenado con el historial de resultados y respuestas ya almacenado en la base:

1. **Modelo de similitud de perfiles**: representa las respuestas de cada test como un vector y
   calcula similitud (coseno / KNN) contra los perfiles de usuarios anteriores para encontrar
   perfiles parecidos y las carreras que esos usuarios terminaron consultando o marcando como
   favoritas.
2. **Agrupamiento de perfiles (clustering)**: identifica grupos de intereses no explícitos en las
   áreas predefinidas (por ejemplo, perfiles mixtos entre dos áreas), mejorando la recomendación
   para casos ambiguos.
3. **Reentrenamiento periódico**: a medida que se acumulan más resultados, el modelo se
   reentrena (script batch) para mejorar su precisión sin intervención manual.
4. **Nueva sección en el resultado**: "Carreras recomendadas por perfiles similares", junto al
   resultado por puntaje ya existente.

### Justificación y beneficios
- **Mejora la precisión** de la recomendación al aprender de datos reales en vez de reglas fijas.
- **Resuelve mejor los perfiles ambiguos** (empate entre áreas), un caso débil del sistema de
  puntaje actual.
- **Valor para el administrador**: con el tiempo, el modelo refleja qué carreras eligen
  realmente los perfiles similares, dato útil para las estadísticas ya existentes.
- **Integra conocimientos de la carrera**: Machine Learning aplicado (scikit-learn), procesamiento
  de datos, diseño de un pipeline de entrenamiento/inferencia e integración con Flask.

### Enfoque técnico

|          Componente          |                          Tecnología propuesta                          |
|-------------------------------|--------------------------------------------------------------------------|
| Modelo de recomendación       | scikit-learn (similitud coseno / KNN + K-Means para clustering)          |
| Entrenamiento                 | Script batch en Python, ejecutado sobre los resultados históricos        |
| Serialización del modelo      | `joblib` (modelo guardado y cargado por la app)                          |
| Integración en el resultado   | Nuevo bloque en `blueprints/sitio/vocacional.py` + template del resultado|
| Datos                         | Reutiliza tablas existentes (`resultados`, `respuestas`, `carreras`); sin romper el esquema actual |
| Autorización                  | Sin cambios (el resultado ya es privado por usuario)                     |

---

## 2. Estimación de horas

### 2.1 Estimación del sistema original (sin la mejora)

|   #  |                                   Tarea                                          |  Horas  |
|------|------------------------------------------------------------------------------------|---------|
|   1  | Relevamiento de requisitos y diseño del modelo de datos                          |   12    |
|   2  | Configuración de la arquitectura (Flask + MySQL + entorno)                       |    8    |
|   3  | Registro, login, roles y recuperación de contraseña                              |   20    |
|   4  | Test vocacional (preguntas, opciones, puntaje, resultados)                       |   25    |
|   5  | Catálogo de carreras, detalle y búsqueda de universidades                        |   18    |
|   6  | Juego interactivo de descubrimiento                                              |   15    |
|   7  | Módulo de noticias (fuentes, filtros de fecha)                                   |   12    |
|   8  | Panel de administración (ABM usuarios, carreras, preguntas, noticias, juego)     |   35    |
|   9  | Exportación de datos a Excel                                                     |   10    |
|  10  | Diseño de interfaz, responsive y temas (claro/oscuro)                            |   15    |
|  11  | Pruebas y correcciones                                                           |   15    |
|  12  | Documentación técnica y despliegue                                               |   10    |
|      | **TOTAL SISTEMA ORIGINAL**                                                       | **195 hs** |

### 2.2 Estimación de la ampliación (nueva mejora: recomendador ML)

|   #  |                                   Tarea                                          |  Horas  |
|------|------------------------------------------------------------------------------------|---------|
|   1  | Análisis y diseño del modelo (enfoque, dataset, criterios de similitud)          |    6    |
|   2  | Preparación y limpieza de datos históricos (extracción de resultados/respuestas) |    8    |
|   3  | Desarrollo y entrenamiento del modelo (similitud + clustering)                   |   20    |
|   4  | Integración del modelo en el backend Flask (carga del modelo, endpoint)          |   12    |
|   5  | Nueva sección en la interfaz de resultado (carreras por perfiles similares)      |    8    |
|   6  | Pruebas, validación de precisión y ajuste de parámetros                          |   10    |
|   7  | Documentación técnica del módulo                                                 |    4    |
|      | **TOTAL AMPLIACIÓN**                                                              | **68 hs**  |

---

## 3. Valor hora

Valor hora definido para el desarrollo: **$ 7.000 ARS / hora**
(desarrollador freelance nivel inicial, mercado Tucumán/Argentina. Este valor es un parámetro
ajustable por el estudiante según su contexto).

---

## 4. Cálculo de costos

|           Concepto                       | Horas |   Valor hora    |        Costo          |
|--------------------------------------------|-------|-----------------|------------------------|
| Costo del sistema original                | 195   |    $ 7.000      |     $ 1.365.000        |
| Costo de la ampliación (mejora)           | 68    |    $ 7.000      |     $   476.000        |
| **Presupuesto total (sistema + mejora)**  | 263   |    $ 7.000      |     $ 1.841.000        |

### Fórmulas utilizadas

```
Costo original    = 195 hs × $ 7.000 = $ 1.365.000
Costo ampliación  =  68 hs × $ 7.000 = $   476.000
Presupuesto total = $ 1.365.000 + $ 476.000 = $ 1.841.000
```

Si se desea recalcular con otro valor hora `V`, el presupuesto total es: **263 hs × V**.

---

## 5. Resumen

- **Mejora propuesta**: Recomendador Inteligente de Carreras basado en Machine Learning (similitud
  de perfiles + clustering), integrado al resultado del test vocacional.
- **Horas de la mejora**: 68 hs.
- **Costo de la mejora**: $ 476.000 ARS.
- **Costo del sistema original**: $ 1.365.000 ARS.
- **Presupuesto total con la mejora**: **$ 1.841.000 ARS**.