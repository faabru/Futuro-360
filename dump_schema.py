import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def dump_schema():
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'futuro360')
        )
        cursor = db.cursor()
        
        tables = ['usuarios', 'carreras', 'tests', 'resultados', 'preguntas', 'opciones_pregunta', 'areas']
        
        for table in tables:
            print(f"\n--- SCHEMA FOR {table} ---")
            cursor.execute(f"SHOW CREATE TABLE {table}")
            print(cursor.fetchone()[1])
            
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    dump_schema()
