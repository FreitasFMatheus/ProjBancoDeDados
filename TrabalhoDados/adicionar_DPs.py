import os
import psycopg2
import random
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

# Seleciona 6 alunos com histórico
cur.execute("""
    SELECT DISTINCT id_aluno FROM Aluno_Turma
""")
alunos_com_historico = [row[0] for row in cur.fetchall()]
alunos_selecionados = random.sample(alunos_com_historico, 6)

print("\n🔁 Adicionando DPs para os seguintes alunos:\n")

for id_aluno in alunos_selecionados:
    cur.execute("""
        SELECT at.id_disciplina, t.periodo, t.ano, t.semestre_ano, t.id_curso
        FROM Aluno_Turma at
        JOIN Turma t ON at.id_turma = t.id_turma
        WHERE at.id_aluno = %s
        ORDER BY t.ano DESC, t.semestre_ano DESC, t.periodo DESC
        LIMIT 1
    """, (id_aluno,))
    resultado = cur.fetchone()
    
    if resultado:
        id_disciplina, periodo, ano, semestre_ano, id_curso = resultado

        novo_periodo = periodo + 1 if periodo < 4 else 1
        novo_ano = ano + 1 if periodo == 4 else ano
        novo_semestre = '2' if semestre_ano == '1' else '1'

        cur.execute("SELECT MAX(id_turma) FROM Turma;")
        max_id = cur.fetchone()[0] or 0
        nova_id_turma = max_id + 1

        # Cria a nova turma com eh_dp = TRUE
        cur.execute("""
            INSERT INTO Turma (id_turma, periodo, ano, semestre_ano, id_curso, eh_dp)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (nova_id_turma, novo_periodo, novo_ano, novo_semestre, id_curso))

        # Cria vínculo com Aluno_Turma
        cur.execute("""
            INSERT INTO Aluno_Turma (id_aluno, id_turma, id_disciplina)
            VALUES (%s, %s, %s)
        """, (id_aluno, nova_id_turma, id_disciplina))

        print(f"🧑 Aluno {id_aluno} -> DP em Disciplina {id_disciplina} na nova Turma {nova_id_turma} ({novo_ano}.{novo_semestre})")

conn.commit()
cur.close()
conn.close()

print("\n✅ DPs adicionadas e vinculadas com sucesso!\n")
