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

# Limpa dados antigos
cur.execute("DELETE FROM Aluno_Turma;")
cur.execute("DELETE FROM Turma;")
cur.execute("DELETE FROM Aluno;")

# Selecionar CPFs dos alunos (excluindo professores)
cur.execute("""
    SELECT cpf FROM Pessoa
    WHERE cpf NOT IN (
        '607.324.851-26', '157.029.483-60', '614.839.027-22', '789.024.315-41',
        '964.183.507-66', '748.613.205-26', '914.275.038-50', '419.350.276-70'
    )
""")
alunos_cpf = [row[0] for row in cur.fetchall()]

# Inserir alunos
for i, cpf in enumerate(alunos_cpf, start=1):
    id_curso = (i % 3) + 1  # 1 = CC, 2 = Elétrica, 3 = CDIA
    cur.execute(
        "INSERT INTO Aluno (id_aluno, cpf, id_curso) VALUES (%s, %s, %s);",
        (i, cpf, id_curso)
    )

# Disciplinas por curso
disciplinas_curso = {
    1: [1, 2, 3, 4],     # CC
    2: [5, 6, 7, 8],     # Elétrica
    3: [9, 10, 11, 12]   # CDIA
}
matematicas = [13, 14, 15, 16]

# Criar turmas
turmas = []
turma_id = 1
anos_semestres = [
    (1, 2024, '1'),
    (2, 2024, '2'),
    (3, 2025, '1'),
    (4, 2025, '2')
]

for periodo, ano, semestre in anos_semestres:
    for curso in [1, 2, 3]:
        turmas.append((turma_id, periodo, ano, semestre, curso, False))  # turma da disciplina do curso
        turma_id += 1
        turmas.append((turma_id, periodo, ano, semestre, curso, False))  # turma de matemática
        turma_id += 1

# Inserir turmas no banco
for turma in turmas:
    cur.execute("""
        INSERT INTO Turma (id_turma, periodo, ano, semestre_ano, id_curso, eh_dp)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, turma)

# Vincular alunos às turmas e disciplinas
for id_aluno in range(1, len(alunos_cpf)+1):
    curso = (id_aluno % 3) + 1
    for idx, (periodo, ano, semestre) in enumerate(anos_semestres):
        cur.execute("""
            SELECT id_turma FROM Turma
            WHERE periodo=%s AND ano=%s AND semestre_ano=%s AND id_curso=%s
            ORDER BY id_turma;
        """, (periodo, ano, semestre, curso))
        resultados = [r[0] for r in cur.fetchall()]
        if len(resultados) < 2:
            continue
        turma_curso, turma_mat = resultados[:2]
        disc_curso = disciplinas_curso[curso][periodo-1]
        disc_mat = matematicas[periodo-1]

        cur.execute("""
            INSERT INTO Aluno_Turma (id_aluno, id_turma, id_disciplina)
            VALUES (%s, %s, %s), (%s, %s, %s);
        """, (id_aluno, turma_curso, disc_curso, id_aluno, turma_mat, disc_mat))

conn.commit()
cur.close()
conn.close()

print("✅ Script executado com sucesso (sem DP, turmas completas por período).")
