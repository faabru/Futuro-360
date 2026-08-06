import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def check_tests():
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'futuro360')
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tests ORDER BY id DESC LIMIT 5")
        tests = cursor.fetchall()
        print("LAST 5 TESTS:")
        for test in tests:
            print(test)
            
        cursor.execute("SELECT * FROM resultados ORDER BY id DESC LIMIT 5")
        res = cursor.fetchall()
        print("\nLAST 5 RESULTADOS:")
        for r in res:
            print(r)
            
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tests()
