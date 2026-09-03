# -*- coding: utf-8 -*-
"""
Actualiza las secciones de `preguntas` y `opciones_pregunta` del dump
`base de datos/futuro 360.sql` con el dataset nuevo (`preguntas_nuevas.py`).

Solo reemplaza las filas INSERT de esas dos tablas; deja intacto el resto del
dump (carreras, áreas, orientaciones, noticias, etc.) y los CREATE TABLE.

Uso:
    python scripts/actualizar_dump_preguntas.py
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.preguntas_nuevas import PREGUNTAS_NUEVAS  # noqa: E402

RUTA_DUMP = os.path.join('base de datos', 'futuro 360.sql')


def escapar(valor):
    texto = str(valor)
    return "'" + texto.replace('\\', '\\\\').replace("'", "''") + "'"


def lineas_preguntas():
    out = []
    for i, p in enumerate(PREGUNTAS_NUEVAS, start=1):
        qid = escapar(p['texto'])
        out.append("INSERT INTO `preguntas` (`id`, `texto_pregunta`, `area_profesional`) "
                   "VALUES (%d, %s, 'General');" % (i, qid))
    return out


def lineas_opciones():
    out = []
    oid = 1
    for i, p in enumerate(PREGUNTAS_NUEVAS, start=1):
        for texto, area in p['opciones']:
            out.append("INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, "
                       "`texto_opcion`, `area_profesional`) VALUES (%d, %d, %s, %s);"
                       % (oid, i, escapar(texto), escapar(area)))
            oid += 1
        # Opción "Ninguna de las anteriores" (Neutral, 0 puntos).
        out.append("INSERT INTO `opciones_pregunta` (`id`, `pregunta_id`, "
                   "`texto_opcion`, `area_profesional`) VALUES (%d, %d, %s, %s);"
                   % (oid, i, escapar('Ninguna de las anteriores'), escapar('Neutral')))
        oid += 1
    return out


def reemplazar_seccion(contenido, tabla, prefix, generar):
    # Localiza el bloque de INSERT de `tabla` (entre su DROP TABLE/CREATE y el
    # siguiente DROP TABLE de otra tabla, o "SET FOREIGN_KEY_CHECKS=1" al final).
    inicio = contenido.index("DROP TABLE IF EXISTS `%s`;" % tabla)
    fin = contenido.find("DROP TABLE IF EXISTS `", inicio + 1)
    if fin == -1:
        fin = contenido.find("SET FOREIGN_KEY_CHECKS=1;")
    bloque = contenido[inicio:fin]

    # Recortar el bloque para quedarnos con las líneas INSERT y reemplazarlas.
    lineas = bloque.split('\n')

    def es_insert(linea):
        return linea.strip().startswith("INSERT INTO `%s`" % tabla)

    insert_indices = [n for n, l in enumerate(lineas) if es_insert(l)]
    if not insert_indices:
        raise RuntimeError('No hay INSERTs de `%s` en el dump.' % tabla)

    primero = insert_indices[0]
    ultimo = insert_indices[-1]

    nuevas = generar()
    bloque_nuevo = lineas[:primero] + nuevas + lineas[ultimo + 1:]
    return contenido[:inicio] + '\n'.join(bloque_nuevo) + contenido[fin:]


def main():
    with io.open(RUTA_DUMP, 'r', encoding='utf-8') as f:
        contenido = f.read()

    contenido = reemplazar_seccion(contenido, 'preguntas', 'preguntas', lineas_preguntas)
    contenido = reemplazar_seccion(contenido, 'opciones_pregunta', 'opciones_pregunta',
                                   lineas_opciones)

    with io.open(RUTA_DUMP, 'w', encoding='utf-8') as f:
        f.write(contenido)

    print('Dump actualizado:', os.path.abspath(RUTA_DUMP))
    print('Preguntas nuevas:', len(PREGUNTAS_NUEVAS))
    print('Opciones nuevas :', len(PREGUNTAS_NUEVAS) * 5)


if __name__ == '__main__':
    main()
