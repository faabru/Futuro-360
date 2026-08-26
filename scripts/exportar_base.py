"""
Exporta la base de contenido actual a `base de datos/futuro 360.sql`.

Genera un dump completo y reimportable: crea las tablas con su esquema actual
(incluidas las columnas agregadas en versiones posteriores) y vuelca los datos
de contenido (carreras, noticias, fuentes, preguntas del juego, orientaciones,
áreas, usuarios de prueba...).

Ese mismo archivo se usa al arrancar la aplicación para auto-crear las tablas
faltantes y sembrar contenido en las que estén vacías (ver
`asegurar_contenido_referencia` en core/migraciones.py).

No incluye cuentas de usuario (cada máquina tiene las suyas), ni datos
personales o transitorios: tests, resultados, códigos de recuperación,
comentarios ni sesiones (esas tablas se crean solas al arrancar).

Uso:
    python scripts/exportar_base.py     (Toma el contenido actual de tu BD (MySQL/Aiven) y
                                        genera un archivo SQL completo , reimportable y exportar todo el contenido a un
                                        archivo" para que la app arranque con datos listos.)
"""

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database_handler import obtener_db

# Tablas cuyo esquema Y datos se exportan (contenido compartido).
# NOTA: `usuarios` NO se exporta a propósito: las cuentas son por máquina
# (se crean con el .env propio o por el registro del sitio), no contenido.
TABLAS_CONTENIDO = [
    'carreras', 'areas',
    'preguntas', 'opciones_pregunta',
    'orientaciones', 'carrera_areas',
    'noticias', 'fuentes', 'fuentes_eliminadas', 'filtros_fecha',
    'game_carreras', 'game_preguntas',
]

# Tablas cuyo esquema se exporta pero quedan vacías (historial del usuario).
TABLAS_VACIAS = ['tests', 'resultados']

RUTA_SALIDA = os.path.join('base de datos', 'futuro 360.sql')


def escapar(valor):
    """Devuelve un valor listo para un literal SQL."""
    if valor is None:
        return 'NULL'
    if isinstance(valor, bool):
        return '1' if valor else '0'
    if isinstance(valor, (int, float)):
        return str(valor)
    texto = str(valor)
    return "'" + texto.replace('\\', '\\\\').replace("'", "''") + "'"


def main():
    with app.app_context():
        db = obtener_db()
        cur = db.cursor()

        salida = io.StringIO()

        salida.write("-- Futuro 360 - dump completo de contenido\n")
        salida.write("-- Generado con scripts/exportar_base.py (no editar a mano).\n")
        salida.write("-- Importar UNA VEZ desde MySQL Workbench (Open SQL Script).\n\n")
        salida.write("CREATE DATABASE IF NOT EXISTS `futuro360` "
                     "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
        salida.write("USE `futuro360`;\n\n")
        salida.write("SET NAMES utf8mb4;\n")
        salida.write("SET FOREIGN_KEY_CHECKS=0;\n\n")

        def volcar(tabla, incluir_datos):
            cur.execute("SHOW CREATE TABLE `%s`" % tabla)
            create = cur.fetchone()[1]
            salida.write("DROP TABLE IF EXISTS `%s`;\n" % tabla)
            salida.write(create + ";\n\n")
            if not incluir_datos:
                return
            cur.execute("SELECT * FROM `%s`" % tabla)
            columnas = [desc[0] for desc in cur.description]
            nombres = ", ".join("`%s`" % c for c in columnas)
            for fila in cur.fetchall():
                valores = ", ".join(escapar(v) for v in fila)
                salida.write("INSERT INTO `%s` (%s) VALUES (%s);\n" % (tabla, nombres, valores))
            salida.write("\n")

        for t in TABLAS_CONTENIDO:
            volcar(t, incluir_datos=True)
        for t in TABLAS_VACIAS:
            volcar(t, incluir_datos=False)

        salida.write("SET FOREIGN_KEY_CHECKS=1;\n")
        salida.write("\n-- Fin del dump\n")

        with io.open(RUTA_SALIDA, 'w', encoding='utf-8') as f:
            f.write(salida.getvalue())

        print('Dump generado en:', os.path.abspath(RUTA_SALIDA))


if __name__ == '__main__':
    main()
