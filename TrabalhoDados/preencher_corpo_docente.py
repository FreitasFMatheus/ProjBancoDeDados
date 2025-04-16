import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Conexão com o banco Supabase
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    sslmode="require"
)
cur = conn.cursor()

# Limpa as tabelas para evitar duplicação
cur.execute("DELETE FROM Professor;")
cur.execute("DELETE FROM Depto;")

# Departamentos
departamentos = {
    1: "Departamento de Computação",
    2: "Departamento de Engenharia Elétrica",
    3: "Departamento de Ciência de Dados e Inteligência Artificial",
    4: "Departamento de Matemática"
}

# Inserir departamentos
for id_depto, nome in departamentos.items():
    cur.execute("INSERT INTO Depto (id_depto, nome) VALUES (%s, %s);", (id_depto, nome))

# Professores com CPFs fixos e departamentos
professores = [
    (1, "607.324.851-26", 1),  # Leo
    (2, "157.029.483-60", 1),  # Charles
    (3, "614.839.027-22", 2),  # Cleiton
    (4, "789.024.315-41", 2),  # André
    (5, "964.183.507-66", 3),  # Leila
    (6, "748.613.205-26", 3),  # Fagner
    (7, "914.275.038-50", 4),  # Elisa
    (8, "419.350.276-70", 4)   # Toninho
]

# Inserir professores
for id_professor, cpf, id_depto in professores:
    cur.execute(
        "INSERT INTO Professor (id_professor, cpf, id_depto) VALUES (%s, %s, %s);",
        (id_professor, cpf, id_depto)
    )

# Definir chefes de departamento
chefes_deptos = {
    1: 1,  # Leo → Computação
    2: 3,  # Cleiton → Elétrica
    3: 5,  # Leila → CDIA
    4: 7   # Elisa → Matemática
}

# Atualizar departamentos com os chefes
for id_depto, id_professor in chefes_deptos.items():
    cur.execute(
        "UPDATE Depto SET chefe_depto = %s WHERE id_depto = %s;",
        (id_professor, id_depto)
    )

# Finaliza
conn.commit()
cur.close()
conn.close()

print("✅ Departamentos, professores e chefes inseridos com sucesso.")
