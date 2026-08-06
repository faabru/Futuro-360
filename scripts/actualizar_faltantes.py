import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'futuro360')
)
cursor = conn.cursor()

updates = [
    # HUMANIDADES
    ("imagenes/humanidades-licenciatura en historia-portada.png",
     "imagenes/humanidades-licenciatura en historia-principal.png",
     "Licenciatura en Historia"),

    ("imagenes/humanidades-licenciatura en letras-portada.png",
     "imagenes/humanidades-licenciatura en letras-principal.png",
     "Licenciatura en Letras"),

    # SALUD MENTAL
    ("imagenes/salud mental-psicopedagogia-portada.jpg",
     "imagenes/salud mental-psicopedagogia-principal.jpg",
     "Psicopedagogía"),

    ("imagenes/salud mental-trabajo social-portada.jpg",
     "imagenes/salud mental-trabajo social-principal.jpg",
     "Trabajo Social"),
]

print("=== ACTUALIZANDO LAS 4 CARRERAS FALTANTES ===")
for portada, principal, nombre in updates:
    try:
        cursor.execute(
            "UPDATE carreras SET imagen_portada = %s, imagen_principal = %s WHERE nombre = %s",
            (portada, principal, nombre)
        )
        if cursor.rowcount > 0:
            print(f"  OK   {nombre}")
        else:
            print(f"  SKIP Sin coincidencia en BD: '{nombre}'")
    except Exception as e:
        print(f"  ERR  ERROR en '{nombre}': {e}")

conn.commit()

print("\n=== VERIFICACION FINAL ===")
cursor.execute('SELECT nombre, imagen_principal FROM carreras ORDER BY nombre')
rows = cursor.fetchall()

ok, miss, nofile = 0, 0, 0
for nombre, ruta in rows:
    if not ruta:
        print(f'  [SIN IMG]  {nombre}')
        miss += 1
    else:
        path = os.path.join('static', ruta)
        if os.path.exists(path):
            ok += 1
        else:
            print(f'  [NO FILE]  {nombre}  ->  {ruta}')
            nofile += 1

print(f'\n=== RESULTADOS ===')
print(f'  Imagenes OK:       {ok}')
print(f'  Sin imagen en BD:  {miss}  (usaran fallback por area)')
print(f'  Archivo no existe: {nofile}')

cursor.close()
conn.close()
