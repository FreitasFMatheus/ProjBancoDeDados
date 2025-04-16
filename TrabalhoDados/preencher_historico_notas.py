import os
import psycopg2
import random
from dotenv import load_dotenv

load_dotenv()

def main():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )
    cur = conn.cursor()

    # Limpar dados antigos (opcional)
    cur.execute("DELETE FROM HistoricoEscolar;")
    cur.execute("DELETE FROM Nota;")
    cur.execute("DELETE FROM Avaliacao;")

    # Seleciona (id_aluno, id_turma, id_disciplina) de Aluno_Turma
    cur.execute("""
        SELECT id_aluno, id_turma, id_disciplina
        FROM Aluno_Turma
        ORDER BY id_aluno, id_turma
    """)
    aluno_turma_disciplinas = cur.fetchall()

    # Vamos pegar todos os alunos distintos
    cur.execute("SELECT DISTINCT id_aluno FROM Aluno_Turma")
    todos_alunos = [row[0] for row in cur.fetchall()]

    # Selecionamos 6 deles para ter notas abaixo de 5
    if len(todos_alunos) > 6:
        alunos_reprovados = random.sample(todos_alunos, 6)
    else:
        # Se tiver 6 ou menos, todos serão reprovados
        alunos_reprovados = todos_alunos

    # Descobre max_id atual de Avaliacao e Nota (pra evitar conflito)
    cur.execute("SELECT COALESCE(MAX(id_avaliacao), 0) FROM Avaliacao;")
    max_id_avaliacao = cur.fetchone()[0]
    next_id_avaliacao = max_id_avaliacao + 1

    cur.execute("SELECT COALESCE(MAX(id_nota), 0) FROM Nota;")
    max_id_nota = cur.fetchone()[0]
    next_id_nota = max_id_nota + 1

    # Para cada (aluno, turma, disciplina) vamos criar Avaliacao, Nota e Historico
    for (id_aluno, id_turma, id_disciplina) in aluno_turma_disciplinas:

        # Gera nota
        if id_aluno in alunos_reprovados:
            nota_valor = random.randint(0, 4)  # 0..4 para reprovado
        else:
            nota_valor = random.randint(5, 10) # 5..10 para aprovado

        # 1) Cria Avaliacao
        cur.execute("""
            INSERT INTO Avaliacao (id_avaliacao, nota, id_disciplina)
            VALUES (%s, %s, %s)
        """, (next_id_avaliacao, nota_valor, id_disciplina))

        # 2) Cria Nota
        # Concluido = True (significa semestre finalizado)
        cur.execute("""
            INSERT INTO Nota (id_nota, id_aluno, id_truma, concluido, id_avaliacao)
            VALUES (%s, %s, %s, %s, %s)
        """, (next_id_nota, id_aluno, id_turma, True, next_id_avaliacao))

        # 3) Cria HistoricoEscolar
        cur.execute("""
            INSERT INTO HistoricoEscolar (id_aluno, id_turma, id_nota)
            VALUES (%s, %s, %s)
        """, (id_aluno, id_turma, next_id_nota))

        next_id_avaliacao += 1
        next_id_nota += 1

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Histórico, Notas e Avaliações preenchidos com sucesso!")

if __name__ == "__main__":
    main()
