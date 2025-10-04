import psycopg
from decouple import config

conection_string = f"dbname={config('DB_NAME')} user={config('DB_USER')} password={config('DB_PASS')} host={config('DB_HOST')} port={config('DB_PORT')}"
conn = psycopg.connect(
    conection_string
)
cur = conn.cursor()
