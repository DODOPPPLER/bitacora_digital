import psycopg

conn = psycopg.connect(
    "dbname=bitacora_digital user=postgres password=Root host=localHost port=5432"
)
cur = conn.cursor()
    