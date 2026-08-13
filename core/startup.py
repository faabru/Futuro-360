"""
Tareas de inicialización de la aplicación.

Funciones que se ejecutan UNA VEZ al arrancar Flask para preparar el entorno
sin intervención manual (por ejemplo, asociar las imágenes de las carreras
que todavía no tienen imagen asignada en la base de datos).
"""

import os

from flask import current_app

from core.migraciones import (
    asegurar_columnas_esquema,
    asegurar_contenido_referencia,
    asegurar_cuenta_dueño,
    asegurar_datos_iniciales,
    asegurar_tabla_areas,
    asegurar_tabla_comentarios,
    asegurar_tabla_filtros_fecha,
    asegurar_tabla_fuentes,
    asegurar_tabla_game_carreras,
    asegurar_tabla_game_preguntas,
    asegurar_tabla_noticias,
    asegurar_tabla_orientaciones,
    asegurar_tabla_password_resets,
    asegurar_tabla_sesiones_activas,
    asegurar_tabla_usuarios,
)
from database_handler import obtener_db


def _normalizar(texto: str) -> str:
    """Normaliza un texto a minúsculas sin tildes ni ñ, para comparaciones."""
    return (texto
            .replace('á', 'a').replace('é', 'e').replace('í', 'i')
            .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
            .strip().lower())


def sincronizar_imagenes():
    """
    Escanea `static/imagenes/` y actualiza los campos `imagen_portada` /
    `imagen_principal` de cada carrera que tenga esos campos en NULL o vacíos.

    No toca registros que ya tienen imagen asignada, por lo que ejecutarlo
    repetidamente no tiene costo apreciable.

    Formato de archivo esperado: `<área>-<nombre>-<portada|principal>.<ext>`
    (por ejemplo: `tecnologia-ingenieria-sistemas-portada.jpg`).
    """
    imagenes_dir = os.path.join(current_app.static_folder, 'imagenes')
    if not os.path.isdir(imagenes_dir):
        print("[imagenes] Directorio de imágenes no encontrado")
        return  # carpeta no existe, nada que hacer

    print(f"[imagenes] Escaneando directorio: {imagenes_dir}")

    # Índice: nombre_archivo_sin_ext_lower → ruta_relativa_a_static.
    index = {}
    for fname in os.listdir(imagenes_dir):
        ruta_relativa = 'imagenes/' + fname
        clave = os.path.splitext(fname)[0].lower()
        index[clave] = ruta_relativa

    print(f"[imagenes] Índice construido con {len(index)} archivos")

    # Índice por nombre de carrera (el nombre es el penúltimo segmento).
    imagenes_por_carrera = {}
    for clave, ruta in index.items():
        partes = [p.strip() for p in clave.split('-')]
        if len(partes) < 3:
            continue  # archivo subido manualmente u otro formato
        nombre_segmento = _normalizar(partes[-2])
        if nombre_segmento not in imagenes_por_carrera:
            imagenes_por_carrera[nombre_segmento] = {'portada': None, 'principal': None}
        if partes[-1].startswith('portada'):
            imagenes_por_carrera[nombre_segmento]['portada'] = ruta
        elif partes[-1].startswith('principal'):
            imagenes_por_carrera[nombre_segmento]['principal'] = ruta

    try:
        conn = obtener_db()
        cursor = conn.cursor(dictionary=True)

        # Solo carreras sin imágenes (optimización: evita tocar las completas).
        cursor.execute("""
            SELECT id, nombre, area_profesional, imagen_portada, imagen_principal
            FROM carreras
            WHERE imagen_portada IS NULL OR imagen_portada = ''
               OR imagen_principal IS NULL OR imagen_principal = ''
        """)
        carreras_sin_imagen = cursor.fetchall()

        print(f"[imagenes] Carreras sin imágenes: {len(carreras_sin_imagen)}")

        if not carreras_sin_imagen:
            cursor.close()
            print("[imagenes] Todas las carreras ya tienen imágenes asignadas")
            return  # nada que hacer

        actualizadas = 0
        for carrera in carreras_sin_imagen:
            nombre_normalized = _normalizar(carrera['nombre'] or '')
            area_normalized = _normalizar(carrera['area_profesional'] or '')

            portada = None
            principal = None

            # Prioridad 1: coincidencia exacta por nombre de la carrera.
            coincidencia = imagenes_por_carrera.get(nombre_normalized)
            if coincidencia:
                portada = coincidencia['portada']
                principal = coincidencia['principal']

            # Prioridad 2: si no hubo coincidencia por nombre, buscar por área.
            if not (portada and principal):
                for clave, ruta in index.items():
                    clave_normalized = _normalizar(clave)
                    if area_normalized and area_normalized in clave_normalized:
                        if 'portada' in clave:
                            portada = ruta
                        elif 'principal' in clave:
                            principal = ruta

            if portada or principal:
                cursor.execute("""
                    UPDATE carreras
                    SET imagen_portada   = COALESCE(NULLIF(imagen_portada, ''), %s),
                        imagen_principal = COALESCE(NULLIF(imagen_principal, ''), %s)
                    WHERE id = %s
                """, (portada, principal, carrera['id']))
                actualizadas += 1
                print(f"[imagenes] Carrera {carrera['id']} ({carrera['nombre']}) "
                      f"actualizada - Portada: {portada}, Principal: {principal}")

        conn.commit()
        cursor.close()

        if actualizadas:
            print(f'[imagenes] Auto-sync: {actualizadas} carreras actualizadas.')
        else:
            print('[imagenes] Auto-sync: sin cambios necesarios.')

    except Exception as e:
        print(f'[imagenes] Auto-sync error (no crítico): {e}')
        import traceback
        traceback.print_exc()


def sincronizar_juego():
    """
    Asegura que todas las carreras del catálogo tengan su tarjeta en el juego
    "Descubre tu Carrera". Se ejecuta al arrancar para que las carreras nunca
    queden fuera del juego aunque la tabla haya quedado vacía.
    """
    try:
        asegurar_tabla_game_carreras()
        print('[juego] Tarjetas de carreras del juego sincronizadas.')
    except Exception as e:
        print(f'[juego] Auto-sync error (no crítico): {e}')


def sincronizar_tablas():
    """
    Asegura que todas las tablas que la aplicación usa existan (idempotente).

    Se ejecuta al arrancar para que una base recién importada quede lista sin
    pasos manuales: `noticias`, `fuentes`, `filtros_fecha`, `orientaciones`,
    preguntas del juego, códigos de recuperación, comentarios y áreas.
    """
    funciones = [
        asegurar_tabla_usuarios,
        asegurar_contenido_referencia,
        asegurar_columnas_esquema,
        asegurar_datos_iniciales,
        asegurar_tabla_noticias,
        asegurar_tabla_fuentes,
        asegurar_tabla_filtros_fecha,
        asegurar_tabla_orientaciones,
        asegurar_tabla_game_preguntas,
        asegurar_tabla_password_resets,
        asegurar_tabla_comentarios,
        asegurar_tabla_areas,
        asegurar_tabla_sesiones_activas,
        asegurar_cuenta_dueño,
    ]
    for fn in funciones:
        try:
            fn()
        except Exception as e:
            print(f'[tablas] Error en {fn.__name__}: {e}')
    print('[tablas] Tablas aseguradas.')
