# Importación de librerías para la conexión con MySQL y manejo de variables de entorno
import mysql.connector
from flask import g
import os
from dotenv import load_dotenv

# Cargar variables de configuración desde el archivo .env
load_dotenv()

# Función para obtener la conexión a la base de datos
# Utiliza el objeto 'g' de Flask para mantener una única conexión por petición
def obtener_db():
    if 'db' not in g:
        # Configuración de los parámetros de conexión
        g.db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'futuro360')
        )
    return g.db

# Función para cerrar la conexión a la base de datos al finalizar la petición
def cerrar_db(e=None):
    # Se extrae la conexión del objeto global 'g' y se cierra si existe
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Función para inicializar la aplicación con el manejador de base de datos
def inicializar_app(app):
    # Registra la función 'cerrar_db' para que se ejecute al terminar el contexto de la aplicación
    app.teardown_appcontext(cerrar_db)
