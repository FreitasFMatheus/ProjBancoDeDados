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

    # 1) Limpar as tabelas TCC e Grupo_TCC
    cur.execute("DELETE FROM TCC;")
    cur.execute("DELETE FROM Grupo_TCC;")

    # 2) Selecionar todos os alunos
    cur.execute("SELECT id_aluno FROM Aluno ORDER BY id_aluno;")
    todos_alunos = [row[0] for row in cur.fetchall()]

    # Seleciona um subset de 24 alunos aleatórios (6 grupos × 4 alunos)
    # Se tiver menos de 24 alunos, pega a quantidade possível
    qtd_alunos_para_tcc = min(24, len(todos_alunos))
    alunos_escolhidos = random.sample(todos_alunos, qtd_alunos_para_tcc)

    # 3) Selecionar todos os professores (para orientador)
    cur.execute("SELECT id_professor FROM Professor ORDER BY id_professor;")
    todos_professores = [row[0] for row in cur.fetchall()]

    # 4) Montar 6 grupos, cada qual com 4 alunos
    num_grupos = qtd_alunos_para_tcc // 4  # deve ser 6 se tivermos 24 alunos
    grupos = []
    index_aluno = 0

    for i in range(num_grupos):
        # Pega 4 alunos
        g_alunos = alunos_escolhidos[index_aluno:index_aluno+4]
        index_aluno += 4
        grupos.append(g_alunos)

    # 5) Inserir grupos e TCC
    # Descobre o próximo id_grupo
    cur.execute("SELECT COALESCE(MAX(id_grupo), 0) FROM Grupo_TCC;")
    max_id_grupo = cur.fetchone()[0]
    next_id_grupo = max_id_grupo + 1

    # Descobre o próximo TCC
    # (Na tabela TCC, não há id, mas usaremos a PK do grupo pra rastrear)
    tcc_count = 0

    for g_alunos in grupos:
        # Cria Grupo_TCC
        # Se tiver menos de 4 alunos no último grupo, completamos com NULL
        aluno1 = g_alunos[0] if len(g_alunos) > 0 else None
        aluno2 = g_alunos[1] if len(g_alunos) > 1 else None
        aluno3 = g_alunos[2] if len(g_alunos) > 2 else None
        aluno4 = g_alunos[3] if len(g_alunos) > 3 else None
        aluno5 = None  # não vamos usar

        cur.execute("""
            INSERT INTO Grupo_TCC (id_grupo, aluno1, aluno2, aluno3, aluno4, aluno5)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (next_id_grupo, aluno1, aluno2, aluno3, aluno4, aluno5))

        # Pega o curso do primeiro aluno só pra gerar um título genérico
        curso_nome = "Algum Curso"
        if aluno1 is not None:
            cur.execute("""
                SELECT c.nome FROM Aluno a
                JOIN Curso c ON a.id_curso = c.id_curso
                WHERE a.id_aluno = %s
            """, (aluno1,))
            row_curso = cur.fetchone()
            if row_curso:
                curso_nome = row_curso[0]

        # Seleciona um orientador aleatório
        orientador = random.choice(todos_professores)

        # Título genérico do TCC
        titulo_tcc = f"TCC de {curso_nome} - Projeto #{next_id_grupo}"

        # Insere TCC
        cur.execute("""
            INSERT INTO TCC (orientador, titulo, id_grupo)
            VALUES (%s, %s, %s)
        """, (orientador, titulo_tcc, next_id_grupo))

        print(f"Grupo TCC #{next_id_grupo}: [{aluno1}, {aluno2}, {aluno3}, {aluno4}] -> {titulo_tcc}")

        next_id_grupo += 1
        tcc_count += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n✅ {tcc_count} TCCs criados com 4 alunos em cada grupo!\n")

if __name__ == "__main__":
    main()
