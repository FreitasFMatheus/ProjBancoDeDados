import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    sslmode="require"
)
cur = conn.cursor()

# Limpar dados antigos
cur.execute("DELETE FROM Disciplina;")
cur.execute("DELETE FROM Curso;")

# Inserir cursos
cursos = [
    (1, "Ciência da Computação", 1, 1),  # depto 1, coordenador Leo (id 1)
    (2, "Ciência de Dados e Inteligência Artificial", 3, 5),  # depto 3, coordenador Leila (id 5)
    (3, "Engenharia Elétrica", 2, 3)  # depto 2, coordenador Cleiton (id 3)
]

for id_curso, nome, id_depto, id_coord in cursos:
    cur.execute(
        "INSERT INTO Curso (id_curso, nome, id_depto, coordenador_curso) VALUES (%s, %s, %s, %s);",
        (id_curso, nome, id_depto, id_coord)
    )

# Inserir disciplinas
disciplinas = [
    # CC
    (1, "Fundamentos de Algoritmos", 1, 1),
    (2, "Banco de Dados", 1, 1),
    (3, "Estrutura de Dados", 1, 2),
    (4, "Complexidade de Algoritmos", 1, 2),

    # CDIA
    (5, "Introdução à Programação", 3, 5),
    (6, "Banco de Dados Avançado", 3, 5),
    (7, "Otimização de Queries", 3, 5),
    (8, "Tratamento de Dados", 3, 5),

    # Elétrica
    (9, "Sistemas Digitais", 2, 3),
    (10, "Redes", 2, 3),
    (11, "Mecânica dos Fluidos", 2, 3),
    (12, "Mecânica dos Sólidos", 2, 3),

    # Matemática (comum a todos)
    (13, "Cálculo 1", 4, 7),  # Elisa
    (14, "Cálculo 2", 4, 7),  # Elisa
    (15, "Cálculo 3", 4, 8),  # Toninho
    (16, "Cálculo 4", 4, 8),  # Toninho
]

for id_disc, nome, id_depto, id_coord in disciplinas:
    cur.execute(
        "INSERT INTO Disciplina (id_disciplina, nome, id_depto, coordenador_disciplina) VALUES (%s, %s, %s, %s);",
        (id_disc, nome, id_depto, id_coord)
    )

conn.commit()
cur.close()
conn.close()

print("✅ Cursos e disciplinas inseridos com sucesso.")
