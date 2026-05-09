import mysql.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()

def simulate_test_save():
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'futuro360')
        )
        cursor = db.cursor(dictionary=True)
        
        # Simulate a logged in user (id=1)
        usuario_id = 1 
        area_ganadora = 'Tecnología'
        area_id = 1
        puntaje_ganador = 10
        detalle_json = json.dumps({"texto": "Prueba de guardado"})

        print("Inserting into tests...")
        cursor.execute("INSERT INTO tests (usuario_id) VALUES (%s)", (usuario_id,))
        id_test = cursor.lastrowid
        print(f"New test ID: {id_test}")

        print("Inserting into resultados...")
        cursor.execute(
            "INSERT INTO resultados (test_id, area_profesional_sugerida, area_id, puntaje, detalle) VALUES (%s, %s, %s, %s, %s)",
            (id_test, area_ganadora, area_id, puntaje_ganador, detalle_json)
        )
        db.commit()
        print("Success!")
        
        cursor.close()
        db.close()
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    simulate_test_save()
