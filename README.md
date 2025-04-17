# ProjBancoDeDados
## Membros

Matheus Ferreira de Freitas  RA: 22.125.085-5 

Henrique Hodel Babler        RA: 22.125.084-8

## Mermaid
Os [Mermaid](https://mermaid.live) foi usado para desenhar os diagramas MR e MER.
### MR
```mermaid
classDiagram
    class PESSOA {
        +cpf: VARCHAR (PK)
        +nome: VARCHAR
    }

    class PROFESSOR {
        +id_professor: INT (PK)
        +cpf: VARCHAR (FK)
        +id_depto: INT (FK)
    }

    class DEPTO {
        +id_depto: INT (PK)
        +nome: VARCHAR
        +chefe_depto: INT (FK)
    }

    class CURSO {
        +id_curso: INT (PK)
        +nome: VARCHAR
        +id_depto: INT (FK)
        +coordenador_curso: INT (FK)
    }

    class ALUNO {
        +id_aluno: INT (PK)
        +cpf: VARCHAR (FK)
        +id_curso: INT (FK)
        +id_turma: INT (FK)
    }

    class DISCIPLINA {
        +id_disciplina: INT (PK)
        +nome: VARCHAR
        +id_depto: INT (FK)
        +coordenador_disciplina: INT (FK)
    }

    class TURMA {
        +id_turma: INT (PK)
        +periodo: INT
        +ano: INT
        +semestre_ano: VARCHAR
        +id_disciplina: INT (FK)
        +id_curso: INT (FK)
        +eh_dp: BOOLEAN
    }

    class AULA {
        +id_aula: INT (PK)
        +id_turma: INT (FK)
        +professor_aula: INT (FK)
    }

    class AVALIACAO {
        +id_avaliacao: INT (PK)
        +nota: INT
        +id_disciplina: INT (FK)
    }

    class NOTA {
        +id_nota: INT (PK)
        +id_aluno: INT (FK)
        +id_turma: INT (FK)
        +concluido: BOOLEAN
        +id_avaliacao: INT (FK)
    }

    class HISTORICO_ESCOLAR {
        +id_aluno: INT (PK,FK)
        +id_turma: INT (PK,FK)
        +id_nota: INT (PK,FK)
    }

    class ALUNO_TURMA {
        +id_turma: INT (PK,FK)
        +id_disciplina: INT (PK,FK)
        +id_aluno: INT (PK,FK)
    }

    class GRUPO_TCC {
        +id_grupo: INT (PK)
        +aluno1: INT (FK)
        +aluno2: INT (FK)
        +aluno3: INT (FK)
        +aluno4: INT (FK)
        +aluno5: INT (FK)
    }

    class TCC {
        +id_grupo: INT (PK,FK)
        +titulo: VARCHAR
        +orientador: INT (FK)
    }

    PESSOA "1" -- "0..1" PROFESSOR
    PESSOA "1" -- "0..1" ALUNO
    DEPTO "1" -- "0..*" PROFESSOR
    DEPTO "1" -- "1..*" CURSO
    DEPTO "1" -- "1..*" DISCIPLINA
    CURSO "1" -- "0..*" ALUNO
    CURSO "1" -- "0..*" TURMA
    DISCIPLINA "1" -- "0..*" TURMA
    PROFESSOR "1" -- "0..*" TCC
    TURMA "1" -- "0..*" AULA
    TURMA "1" -- "0..*" NOTA
    ALUNO "1" -- "0..*" NOTA
    AVALIACAO "1" -- "1..*" NOTA
    ALUNO "1" -- "0..*" HISTORICO_ESCOLAR
    ALUNO "1" -- "0..1" GRUPO_TCC
```
### MER

```mermaid

erDiagram
    PESSOA {
        VARCHAR cpf PK
        VARCHAR nome
    }

    PROFESSOR {
        INT id_professor PK
        VARCHAR cpf FK
        INT id_depto FK
    }

    DEPTO {
        INT id_depto PK
        VARCHAR nome
        INT chefe_depto FK
    }

    CURSO {
        INT id_curso PK
        VARCHAR nome
        INT id_depto FK
        INT coordenador_curso FK
    }

    DISCIPLINA {
        INT id_disciplina PK
        VARCHAR nome
        INT id_depto FK
        INT coordenador_disciplina FK
    }

    ALUNO {
        INT id_aluno PK
        VARCHAR cpf FK
        INT id_curso FK
    }

    TURMA {
        INT id_turma PK
        INT periodo
        INT ano
        VARCHAR semestre_ano
        INT id_curso FK
        BOOLEAN eh_dp
    }

    AULA {
        INT id_aula PK
        INT id_turma FK
        INT professor_aula FK
    }

    AVALIACAO {
        INT id_avaliacao PK
        INT nota
        INT id_disciplina FK
    }

    NOTA {
        INT id_nota PK
        INT id_aluno FK
        INT id_turma FK
        BOOLEAN concluida
        INT id_avaliacao FK
    }

    HISTORICOESCOLAR {
        INT id_aluno PK, FK
        INT id_turma PK, FK
        INT id_nota PK, FK
    }

    ALUNO_TURMA {
        INT id_aluno PK, FK
        INT id_turma PK, FK
        INT id_disciplina PK, FK
    }

    GRUPO_TCC {
        INT id_grupo PK
        INT aluno1 FK
        INT aluno2 FK
        INT aluno3 FK
        INT aluno4 FK
        INT aluno5 FK
    }

    TCC {
        INT id_grupo PK, FK
        VARCHAR titulo
        INT orientador FK
    }

    %% RELACIONAMENTOS COM TODAS AS REGRAS APLICADAS
    PESSOA ||--|| PROFESSOR : pode_ser
    PESSOA ||--o{ ALUNO : possui_matriculas

    PROFESSOR ||--|| DEPTO : pertence
    PROFESSOR ||--|| CURSO : coordena
    PROFESSOR ||--|| DISCIPLINA : coordena
    PROFESSOR ||--|| AULA : ministra
    PROFESSOR ||--|| TCC : orienta

    DEPTO ||--|| CURSO : possui
    DEPTO ||--|| DISCIPLINA : oferece
    DEPTO ||--|| PROFESSOR : chefiado_por

    CURSO ||--|| TURMA : organiza
    CURSO ||--|| ALUNO : matricula

    TURMA ||--|| AULA : possui
    TURMA ||--|| NOTA : registra
    TURMA ||--|| ALUNO_TURMA : contem
    TURMA ||--|| HISTORICOESCOLAR : compoe

    DISCIPLINA ||--|| AVALIACAO : possui
    DISCIPLINA ||--|| ALUNO_TURMA : pertence

    AVALIACAO ||--|| NOTA : avalia

    ALUNO ||--o{ ALUNO_TURMA : estuda
    ALUNO ||--o{ NOTA : recebe
    ALUNO ||--o{ GRUPO_TCC : participa

    GRUPO_TCC ||--|| TCC : compoe


```



## Como popular rapidamente o banco de dados

1. *preencher_pessoa.py*  
   Cria 8 pessoas fixas (professores) + 60 pessoas aleatórias (CPFs e nomes).

2. *preencher_corpo_docente.py*  
   Cadastra departamentos, insere os 8 professores e define o chefe de cada depto.

3. *formar_turmas.py*  
   Distribui os 60 alunos em três cursos, gera 40 turmas e matricula cada aluno
   de acordo com o período. Também inclui alguns exemplos de dependência (DP) (o qual não conseguimos executar precisamente da maneira descrita).

4. *aulas.py*  
   Liga cada turma a um professor, criando as aulas.

5. *preencher_grade_curricular.py*  
   Garante todas as disciplinas dos cursos, associadas ao departamento correto
   e a um professor coordenador.

6. *preencher_historico_notas.py*  
   Gera avaliações, notas (aprovado/reprovado) e preenche o histórico escolar.

> Execute esses scripts nessa ordem para ter um banco completo e coerente para testes.
