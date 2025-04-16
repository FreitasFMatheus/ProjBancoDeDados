import os
import psycopg2
from dotenv import load_dotenv
from faker import Faker

# Carrega variáveis de ambiente do .env
load_dotenv()
fake = Faker("pt_BR")

# Conecta ao banco Supabase
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    sslmode="require"
)
cur = conn.cursor()

# Nomes fixos
nomes_fixos = ["Leo", "Charles", "Cleiton", "André", "Leila", "Fagner", "Elisa", "Toninho"]

# Inserir nomes fixos com CPFs únicos
for nome in nomes_fixos:
    cpf = fake.unique.cpf()
    cur.execute("INSERT INTO Pessoa (cpf, nome) VALUES (%s, %s);", (cpf, nome))

# Inserir 60 pessoas com nomes aleatórios
for _ in range(60):
    nome = fake.name()
    cpf = fake.unique.cpf()
    cur.execute("INSERT INTO Pessoa (cpf, nome) VALUES (%s, %s);", (cpf, nome))

# Commit e fechar conexão
conn.commit()
cur.close()
conn.close()

print("✅ Tabela Pessoa preenchida com sucesso (68 registros).")
