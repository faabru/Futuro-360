"""
Script para actualizar imagen_portada e imagen_principal de todas las carreras.
Usa los nombres de archivo EXACTOS del filesystem (static/imagenes/).
Ejecutar desde la raíz del proyecto: python actualizar_imagenes.py
"""
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'futuro360')
)
cursor = conn.cursor()

# Rutas relativas desde static/ — nombres exactos del filesystem
updates = [
    # AGRONOMÍA  (nota: el archivo tiene espacio extra antes del guión)
    ("imagenes/agronomia-ingenieria agronomica -portada.jpg",
     "imagenes/agronomia-ingenieria agronomica -principal.jpg",
     "Ingeniería Agronómica"),

    ("imagenes/agronomia-ingenieria forestal -portada.jpg",
     "imagenes/agronomia-ingenieria forestal -principal.jpg",
     "Ingeniería Forestal"),

    ("imagenes/agronomia-medicina veterinaria-portada.jpg",
     "imagenes/agronomia-medicina veterinaria-principal.jpg",
     "Medicina Veterinaria"),

    ("imagenes/agronomia-Tecnicatura en Producción Agropecuaria-portada.jpg",
     "imagenes/agronomia-Tecnicatura en Producción Agropecuaria-principal.jpg",
     "Tecnicatura en Producción Agropecuaria"),

    # ARTE Y DISEÑO
    ("imagenes/arte y diseño-arquitectura-portada.jpg",
     "imagenes/arte y diseño-arquitectura-principal.jpg",
     "Arquitectura"),

    ("imagenes/arte y diseño-diseño grafico-portada.jpg",
     "imagenes/arte y diseño-diseño grafico-principal.jpg",
     "Diseño Gráfico"),

    ("imagenes/arte y diseño-Licenciatura en Artes Visuales-portada.jpg",
     "imagenes/arte y diseño-Licenciatura en Artes Visuales-principal.jpg",
     "Licenciatura en Artes Visuales"),

    ("imagenes/arte y diseño-musica-portada.jpg",
     "imagenes/arte y diseño-musica-principal.jpg",
     "Música"),

    # CIENCIAS NATURALES
    ("imagenes/ciencias naturales-biologia-portada.jpg",
     "imagenes/ciencias naturales-biologia-principal.jpg",
     "Biología"),

    ("imagenes/ciencias naturales-geologia-portada.jpg",
     "imagenes/ciencias naturales-geologia-principal.jpg",
     "Geología"),

    ("imagenes/ciencias naturales-quimica-portada.jpg",
     "imagenes/ciencias naturales-quimica-principal.jpg",
     "Química"),

    # COMUNICACIÓN
    ("imagenes/comunicación-Licenciatura en Comunicación Social-portada.jpg",
     "imagenes/comunicación-Licenciatura en Comunicación Social-principal.jpg",
     "Licenciatura en Comunicación Social"),

    ("imagenes/comunicación-periodismo-portada.jpg",
     "imagenes/comunicación-periodismo-principal.jpg",
     "Periodismo"),

    ("imagenes/comunicación-publicidad-portada.jpg",
     "imagenes/comunicación-publicidad-principal.jpg",
     "Publicidad"),

    # DERECHO
    ("imagenes/derecho-abogacia-portada.jpg",
     "imagenes/derecho-abogacia-principal.jpg",
     "Abogacía"),

    ("imagenes/derecho-ciencias politicas-portada.jpg",
     "imagenes/derecho-ciencias politicas-principal.jpg",
     "Ciencias Políticas"),

    ("imagenes/derecho-notariado-portada.jpg",
     "imagenes/derecho-notariado-principal.jpg",
     "Notariado"),

    # HUMANIDADES
    ("imagenes/humanidades-licenciatura en filosofia-portada.jpg",
     "imagenes/humanidades-licenciatura en filosofia-principal.jpg",
     "Licenciatura en Filosofía"),

    # INGENIERÍA
    ("imagenes/ingenieria-ingenieria civil-portada.jpg",
     "imagenes/ingenieria-ingenieria civil-principal.jpg",
     "Ingeniería Civil"),

    ("imagenes/ingenieria-ingenieria electrica-portada.jpg",
     "imagenes/ingenieria-ingenieria electrica-principal.jpg",
     "Ingeniería Eléctrica"),

    ("imagenes/ingenieria-ingenieria industrial-portada.jpg",
     "imagenes/ingenieria-ingenieria industrial-principal.jpg",
     "Ingeniería Industrial"),

    ("imagenes/ingenieria-ingenieria mecanica-portada.jpg",
     "imagenes/ingenieria-ingenieria mecanica-principal.jpg",
     "Ingeniería Mecánica"),

    ("imagenes/ingenieria-ingenieria quimica-portada.jpg",
     "imagenes/ingenieria-ingenieria quimica-principal.jpg",
     "Ingeniería Química"),

    # NEGOCIOS
    ("imagenes/negocios-contador publico nacional-portada.jpg",
     "imagenes/negocios-contador publico nacional-principal.jpg",
     "Contador Público Nacional"),

    ("imagenes/negocios-licenciatura en administracion-portada.jpg",
     "imagenes/negocios-licenciatura en administracion-principal.jpg",
     "Licenciatura en Administración"),

    ("imagenes/negocios-licenciatura en economia-portada.jpg",
     "imagenes/negocios-licenciatura en economia-principal.jpg",
     "Licenciatura en Economía"),

    ("imagenes/negocios-marketing digital-portada.jpg",
     "imagenes/negocios-marketing digital-principal.jpg",
     "Marketing Digital"),

    # SALUD MENTAL
    ("imagenes/salud mental-Psicología-portada.jpg",
     "imagenes/salud mental-Psicología-principal.jpg",
     "Psicología"),

    # SALUD
    ("imagenes/salud-Kinesiología y Fisioterapia-portada.jpg",
     "imagenes/salud-Kinesiología y Fisioterapia-principal.jpg",
     "Kinesiología y Fisioterapia"),

    ("imagenes/salud-bioquimica-portada.jpg",
     "imagenes/salud-bioquimica-principal.jpg",
     "Bioquímica"),

    ("imagenes/salud-enfermeria-portada.jpg",
     "imagenes/salud-enfermeria-principal.jpg",
     "Enfermería"),

    ("imagenes/salud-farmacia-portada.jpg",
     "imagenes/salud-farmacia-principal.jpg",
     "Farmacia"),

    ("imagenes/salud-medicina-portada.jpg",
     "imagenes/salud-medicina-principal.jpg",
     "Medicina"),

    ("imagenes/salud-nutrición-portada.jpg",
     "imagenes/salud-nutrición-principal.jpg",
     "Nutrición"),

    ("imagenes/salud-odontologia-portada.jpg",
     "imagenes/salud-odontologia-principal.jpg",
     "Odontología"),

    # TECNOLOGÍA
    ("imagenes/tecnologia-Ingeniería en Sistemas de Información-portada.jpg",
     "imagenes/tecnologia-Ingeniería en Sistemas de Información-principal.jpg",
     "Ingeniería en Sistemas de Información"),

    ("imagenes/tecnologia-Licenciatura en Sistemas de Información-portada.jpg",
     "imagenes/tecnologia-Licenciatura en Sistemas de Información-principal.jpg",
     "Licenciatura en Sistemas de Información"),

    ("imagenes/tecnologia-Tecnicatura en Programación-portada.jpg",
     "imagenes/tecnologia-Tecnicatura en Programación-principal.jpg",
     "Tecnicatura en Programación"),
]

ok = 0
skip = 0
errors = []

for portada, principal, nombre in updates:
    try:
        cursor.execute(
            "UPDATE carreras SET imagen_portada = %s, imagen_principal = %s WHERE nombre = %s",
            (portada, principal, nombre)
        )
        if cursor.rowcount > 0:
            print(f"  OK   {nombre}")
            ok += 1
        else:
            print(f"  SKIP Sin coincidencia en BD: '{nombre}'")
            skip += 1
    except Exception as e:
        print(f"  ERR  ERROR en '{nombre}': {e}")
        errors.append(nombre)

conn.commit()
cursor.close()
conn.close()

print(f"\n{'='*50}")
print(f"  Actualizadas: {ok}")
print(f"  Sin match:    {skip}")
print(f"  Errores:      {len(errors)}")
if errors:
    print(f"  Fallos: {errors}")
print(f"{'='*50}")
