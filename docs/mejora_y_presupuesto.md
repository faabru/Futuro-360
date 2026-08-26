# Futuro 360 — Propuesta y Presupuesto

## 1. Mejoras propuestas

#### 1.1 Recomendador Inteligente de Carreras (Machine Learning)

**Situación actual:** el test vocacional calcula el resultado con un puntaje acumulado por área (suma simple de respuestas): el área con más puntos define la recomendación de carreras. Es un enfoque basado en reglas fijas, sin aprendizaje ni ajuste a partir del comportamiento real de los usuarios.

**Alcance:**
1. **Modelo de similitud de perfiles**: representa las respuestas de cada test como un vector y calcula similitud (coseno / KNN) contra perfiles anteriores para encontrar perfiles parecidos y las carreras que esos usuarios terminaron consultando o marcando como favoritas.
2. **Agrupamiento de perfiles (clustering)**: identifica grupos de intereses no explícitos en las áreas predefinidas, mejorando la recomendación para perfiles mixtos o ambiguos.
3. **Reentrenamiento periódico**: a medida que se acumulan más resultados, el modelo se reentrena (script batch) para mejorar su precisión sin intervención manual.
4. **Nueva sección en el resultado**: "Carreras recomendadas por perfiles similares".

**Tecnología:** scikit-learn (similitud coseno / KNN + K-Means), entrenamiento batch en Python, modelo serializado con `joblib`, sin cambios de esquema en la base de datos.

#### 1.2 Buscador de universidades propio (reemplazo de DuckDuckGo)

**Situación actual:** la búsqueda de universidades usa un buscador gratuito de terceros (DuckDuckGo vía la librería `ddgs`), sin garantía de disponibilidad, límites de uso ni control sobre la calidad de los resultados.

**Alcance:** reemplazar esa dependencia por un proveedor de búsqueda profesional y pago (API de búsqueda con SLA, por ejemplo Google Programmable Search o Bing Search API), con resultados más estables y filtrados específicamente para instituciones educativas. Incluye la migración del código que arma las consultas y procesa los resultados.

**Tecnología:** API de búsqueda paga (a definir proveedor), capa de caché de resultados para reducir consumo de cuota.

#### 1.3 Proveedor único de envío de correo

**Situación actual:** el sistema usa dos proveedores distintos para emails (uno para los correos transaccionales — PIN de recuperación, avisos de cuenta — y otro para el formulario de contacto), lo que duplica configuración, credenciales y puntos de falla.

**Alcance:** unificar todo el envío de correo (transaccionales y de contacto/soporte) en un único proveedor pago de nivel profesional (por ejemplo SendGrid, Mailgun o Amazon SES), con mejor entregabilidad, estadísticas de envío y un solo panel de administración.

#### 1.4 Escalado de base de datos (mayor concurrencia)

**Situación actual:** el plan gratuito de la base de datos limita la cantidad de conexiones simultáneas, lo que obliga a mantener pocos procesos del servidor corriendo a la vez y restringe cuántas solicitudes de una misma función se pueden atender al mismo tiempo.

**Alcance:** migrar a un plan pago de base de datos con mayor límite de conexiones, e implementar un **pool de conexiones** en el backend para aprovecharlo (en vez de abrir una conexión nueva por cada solicitud). Incluye el ajuste del número de procesos del servidor y pruebas de carga.

#### 1.5 Asistente de IA de ayuda al estudiante

**Alcance:** un asistente conversacional integrado en la plataforma que responde dudas del estudiante sobre carreras, el resultado de su test, cómo usar el sitio y orientación general, disponible como un chat accesible desde cualquier pantalla del sitio público.

**Tecnología:** integración con la API de un proveedor de inteligencia artificial, endpoint propio en el backend para gestionar la conversación y el contexto del usuario, y un widget de chat en el frontend.

---

## 2. Estimación de horas

#### 2.1 Sistema base (plataforma completa)

| #  | Tarea                                                                        | Horas   |
|----|------------------------------------------------------------------------------|---------|
| 1  | Relevamiento de requisitos y diseño del modelo de datos                      | 12      |
| 2  | Configuración de la arquitectura (Flask + MySQL + entorno)                   | 8       |
| 3  | Registro, login, roles y recuperación de contraseña                          | 20      |
| 4  | Test vocacional (preguntas, opciones, puntaje, resultados)                   | 25      |
| 5  | Catálogo de carreras, detalle y búsqueda de universidades                    | 18      |
| 6  | Juego interactivo de descubrimiento                                          | 15      |
| 7  | Módulo de noticias (fuentes, filtros de fecha)                               | 12      |
| 8  | Panel de administración (ABM usuarios, carreras, preguntas, noticias, juego) | 35      |
| 9  | Exportación de datos a Excel                                                 | 10      |
| 10 | Diseño de interfaz, responsive y temas (claro/oscuro)                        | 15      |
| 11 | Pruebas y correcciones                                                       | 15      |
| 12 | Documentación técnica y despliegue                                           | 10      |
|    | **TOTAL SISTEMA BASE**                                                       | **195** |

#### 2.2 Ampliaciones

**Recomendador Inteligente (ML)**

| # | Tarea                                                                   | Horas  |
|---|-------------------------------------------------------------------------|--------|
| 1 | Análisis y diseño del modelo (enfoque, dataset, criterios de similitud) | 6      |
| 2 | Preparación y limpieza de datos históricos                              | 8      |
| 3 | Desarrollo y entrenamiento del modelo (similitud + clustering)          | 20     |
| 4 | Integración del modelo en el backend                                    | 12     |
| 5 | Nueva sección en la interfaz de resultado                               | 8      |
| 6 | Pruebas y ajuste de parámetros                                          | 10     |
| 7 | Documentación técnica del módulo                                        | 4      |
|   | **Subtotal**                                                            | **68** |

**Buscador de universidades propio**

| # | Tarea                                                     | Horas  |
|---|-----------------------------------------------------------|--------|
| 1 | Evaluación y selección del proveedor de búsqueda          | 3      |
| 2 | Integración de la nueva API y migración del código actual | 9      |
| 3 | Capa de caché de resultados                               | 3      |
| 4 | Pruebas y ajustes                                         | 3      |
|   | **Subtotal**                                              | **18** |

**Proveedor único de correo**

| # | Tarea                                                             | Horas  |
|---|-------------------------------------------------------------------|--------|
| 1 | Evaluación y selección del proveedor                              | 3      |
| 2 | Migración de plantillas y flujos de envío existentes              | 8      |
| 3 | Pruebas de entrega (recuperación de contraseña, avisos, contacto) | 5      |
|   | **Subtotal**                                                      | **16** |

**Escalado de base de datos**

| # | Tarea                                                    | Horas  |
|---|----------------------------------------------------------|--------|
| 1 | Implementación de pool de conexiones en el backend       | 5      |
| 2 | Ajuste de procesos del servidor y configuración del plan | 2      |
| 3 | Pruebas de carga y concurrencia                          | 3      |
|   | **Subtotal**                                             | **10** |

**Asistente de IA de ayuda al estudiante**

| # | Tarea                                        | Horas  |
|---|----------------------------------------------|--------|
| 1 | Diseño de la conversación y casos de uso     | 6      |
| 2 | Integración con el proveedor de IA y backend | 14     |
| 3 | Widget de chat en el frontend                | 10     |
| 4 | Pruebas y ajustes                            | 6      |
|   | **Subtotal**                                 | **36** |

**TOTAL AMPLIACIONES: 148 hs**

---

## 3. Valor hora

Valor hora de desarrollo: **$ 7.000 ARS / hora**

---

## 4. Presupuesto de desarrollo

| Concepto                            | Horas   | Valor hora | Costo           |
|-------------------------------------|---------|------------|-----------------|
| Sistema base                        | 195     | $ 7.000    | $ 1.365.000     |
| Recomendador ML                     | 68      | $ 7.000    | $ 476.000       |
| Buscador de universidades propio    | 18      | $ 7.000    | $ 126.000       |
| Proveedor único de correo           | 16      | $ 7.000    | $ 112.000       |
| Escalado de base de datos           | 10      | $ 7.000    | $ 70.000        |
| Asistente de IA para el estudiante  | 36      | $ 7.000    | $ 252.000       |
| **PRESUPUESTO TOTAL DE DESARROLLO** | **343** | $ 7.000    | **$ 2.401.000** |

```
Presupuesto total = 343 hs × $ 7.000 = $ 2.401.000
```

---

## 5. Costos de infraestructura y servicios (mensuales, recurrentes)

Son valores de referencia; el valor final se define al contratar cada servicio según el plan y el volumen de uso real de la plataforma.

| Servicio                              | Motivo                                         | Estimado mensual (USD) |
|---------------------------------------|--------------------------------------- --------|------------------------|
| Proveedor de búsqueda pago            | Buscador de universidades propio               | 5 – 30                 |
| Proveedor único de correo (plan pago) | Envío de correos transaccionales y de contacto | 15 – 20                |
| Plan pago de base de datos            | Más conexiones simultáneas                     | 19 – 30                |
| API de inteligencia artificial        | Asistente de ayuda al estudiante               | 10 – 30 (según uso)    |

---

## 6. Resumen ejecutivo

- **Producto:** Futuro 360, plataforma de orientación vocacional (test vocacional, catálogo de carreras, juego interactivo, noticias, panel de administración con estadísticas y reportes).
- **Mejoras incluidas en esta propuesta:** recomendador inteligente por Machine Learning, buscador de universidades propio, proveedor único de correo, escalado de base de datos y asistente de IA de ayuda al estudiante.
- **Horas totales de desarrollo:** 343 hs.
- **Presupuesto total de desarrollo:** **$ 2.401.000 ARS**.
- **Costos recurrentes estimados:** entre USD 49 y USD 110 por mes, según los proveedores y planes elegidos.