import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def check_questions():
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'futuro360')
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM preguntas LIMIT 5")
        qs = cursor.fetchall()
        print("PREGUNTAS:")
        for q in qs:
            print(q)
            
        cursor.execute("SELECT * FROM opciones_pregunta LIMIT 5")
        opts = cursor.fetchall()
        print("\nOPCIONES:")
        for o in opts:
            print(o)
            
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_questions()
