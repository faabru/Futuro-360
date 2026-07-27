# Templates individuales por carrera — Futuro 360

## ¿Cómo funciona?

Cuando el usuario entra a `/carrera/ID`, Flask verifica si existe
el archivo `templates/carreras/carrera_ID.html`.

- Si **EXISTE** → usa ese template personalizado
- Si **NO existe** → usa `templates/carrera_detalle.html` (genérico)

Ninguna carrera queda sin página. El sistema es **aditivo**: agregar
un nuevo template nunca rompe las carreras que no lo tienen.

---

## ¿Cómo agregar una nueva carrera personalizada?

1. Copiá el archivo `_base_carrera.html`
2. Renombralo como `carrera_ID.html`
   *(ID = número de la carrera en la tabla `carreras` de MySQL)*
3. Personalizá las secciones marcadas con `▸ PERSONALIZAR ◂`:
   - **Imagen**: reemplazá la URL de Unsplash por una específica de esa carrera
   - **¿A qué se dedica?**: escribí un párrafo propio (no el genérico de la BD)
   - Podés agregar secciones extra: salidas laborales, duración, links, etc.
4. Guardá el archivo en esta carpeta — Flask lo detecta automáticamente al recargar

> **No hace falta reiniciar el servidor** si Flask está en modo debug (`debug=True`).

---

## ¿Cómo saber el ID de una carrera?

**Opción A — Panel admin:**
```
/admin/carreras
```

**Opción B — Consulta SQL directa:**
```sql
SELECT id, nombre, area_profesional
FROM carreras
ORDER BY id;
```

---

## IDs más comunes

| ID | Carrera                              | Área               |
|----|--------------------------------------|--------------------|
| 1  | Ingeniería en Sistemas de Información | Tecnología        |
| 4  | Ingeniería Civil                     | Ingeniería         |
| 9  | Medicina                             | Salud              |
| 11 | Odontología                          | Salud              |
| 16 | Psicología                           | Salud Mental       |
| 22 | Ingeniería Agronómica                | Agronomía          |
| 26 | Contador Público Nacional            | Negocios           |
| 30 | Abogacía                             | Derecho            |
| 36 | Diseño Gráfico                       | Arte y Diseño      |
| 39 | Arquitectura ✅ *(ya personalizada)* | Arte y Diseño      |

---

## ⚠ IMPORTANTE: el buscador DuckDuckGo

La ruta `/carrera/<id>/buscar-universidades` devuelve JSON con campo **`url`** (no `link`).

Siempre que copies el template base, verificá que el `fetch` use `r.url`:

```javascript
data.resultados.forEach(r => {
    html += `<li class="list-group-item px-0 border-0 py-2">
        <a href="${r.url}" target="_blank">${r.titulo}</a>
    </li>`;
});
```

> **Nunca usar** `r.link`, `item.link` ni `r.href` — la API de DDGS devuelve `href`
> internamente, pero la ruta Flask lo mapea a `url` antes de enviarlo al frontend.

---

## Estructura de la respuesta JSON del buscador

```json
{
  "resultados": [
    {
      "titulo": "UNT - Facultad de Arquitectura y Urbanismo",
      "url": "https://fau.unt.edu.ar",
      "descripcion": "Facultad de Arquitectura de la Universidad Nacional de Tucumán..."
    }
  ],
  "total": 5,
  "status": "success"
}
```

---

## Estructura de archivos

```
templates/
├── carrera_detalle.html        ← genérico (fallback, no modificar)
└── carreras/
    ├── README.md               ← este archivo
    ├── _base_carrera.html      ← modelo de referencia (copiar para nuevas carreras)
    └── carrera_39.html         ← Arquitectura (ejemplo funcional)
```
