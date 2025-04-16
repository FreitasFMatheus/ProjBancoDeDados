import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )

    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("🎉 Conectado com sucesso ao banco Supabase!")
    print("Versão do PostgreSQL:", cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Erro ao conectar:", e)
