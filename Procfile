# LIMITACIÓN DE WORKERS (Aiven free tier):
# El plan gratuito de Aiven MySQL permite ~10 conexiones simultáneas. Cada
# worker de gunicorn maneja varias requests y cada request abre UNA conexión
# a la BD (ver database_handler.py). Con 2 workers se mantiene el uso de
# conexiones bajo el límite sin agotarlas.
#
# Si se aumenta --workers (más tráfico), también hay que subir el límite de
# conexiones en Aiven (plan pagado) o migrar a un pool de conexiones
# (MySQLConnectionPool, ver ejemplo comentado en database_handler.py).
web: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT --timeout 120
