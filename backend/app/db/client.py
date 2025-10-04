import psycopg
from decouple import config

conection_string = f"dbname=bitacora_digital user={config('DB_USER')} password={config('DB_PASS')} host={config('DB_HOST')} port=5432"
conn = psycopg.connect(
    conection_string
)
cur = conn.cursor()

    