import os
import psycopg2
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

    # (Opcional) Limpa a tabela Aula para evitar duplicações
    cur.execute("DELETE FROM Aula;")

    # Vamos buscar todas as combinações (turma, disciplina) que já existem no Aluno_Turma
    # e descobrir quem é o professor coordenador daquela disciplina
    cur.execute("""
        SELECT DISTINCT 
            t.id_turma, 
            d.coordenador_disciplina
        FROM Aluno_Turma at
        JOIN Turma t 
            ON at.id_turma = t.id_turma
        JOIN Disciplina d
            ON at.id_disciplina = d.id_disciplina
        ORDER BY t.id_turma
    """)
    resultados = cur.fetchall()

    # Começamos o id_aula a partir do último valor existente (ou 0 se não tiver nada)
    cur.execute("SELECT COALESCE(MAX(id_aula), 0) FROM Aula;")
    max_aula = cur.fetchone()[0]
    proximo_id_aula = max_aula + 1

    for (id_turma, id_professor) in resultados:
        # Se esse 'id_professor' for nulo ou não existir, você pode tratar aqui (ex: pular)
        # Caso esteja tudo certo, faz a inserção da aula
        cur.execute("""
            INSERT INTO Aula (id_aula, id_turma, professor_aula)
            VALUES (%s, %s, %s)
        """, (proximo_id_aula, id_turma, id_professor))

        proximo_id_aula += 1

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Aulas criadas com sucesso!")

if __name__ == "__main__":
    main()
