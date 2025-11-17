# alunos/test/test_crud_mock.py

import pytest
from unittest.mock import Mock

# ===================== MOCK DAS MODELS =====================

class UserMock:
    def __init__(self, username):
        self.username = username

class AlunoMock:
    def __init__(self, user, matricula):
        self.user = user
        self.matricula = matricula

class ProfessorMock:
    def __init__(self, user):
        self.user = user

class AvaliacaoMock:
    _db = []

    def __init__(self, aluno, professor, nota_b1, nota_b2, faltas):
        self.aluno = aluno
        self.professor = professor
        self.nota_b1 = nota_b1
        self.nota_b2 = nota_b2
        self.faltas = faltas
        self.media = (nota_b1 + nota_b2) / 2
        self.status = self.calcular_status()
        self.id = len(AvaliacaoMock._db) + 1

    def calcular_status(self):
        if self.faltas > 15:
            return "Reprovado por faltas"
        elif self.media < 7.0:
            return "Reprovado"
        else:
            return "Aprovado"

    def save(self):
        AvaliacaoMock._db.append(self)

    def delete(self):
        AvaliacaoMock._db = [a for a in AvaliacaoMock._db if a.id != self.id]

    @classmethod
    def get(cls, id):
        for a in cls._db:
            if a.id == id:
                return a
        raise ValueError("Avaliacao não encontrada")

    @classmethod
    def clear_db(cls):
        cls._db = []

# ===================== FIXTURES =====================

@pytest.fixture
def aluno_professor_mock():
    user_aluno = UserMock("aluno")
    aluno = AlunoMock(user_aluno, "12345678")
    user_prof = UserMock("professor")
    professor = ProfessorMock(user_prof)
    return aluno, professor

@pytest.fixture(autouse=True)
def clear_avaliacao_db():
    AvaliacaoMock.clear_db()
    yield
    AvaliacaoMock.clear_db()

# ===================== TESTES =====================

def test_create_avaliacao_valida(aluno_professor_mock):
    aluno, professor = aluno_professor_mock
    av = AvaliacaoMock(aluno, professor, 8.0, 7.5, 2)
    av.save()
    assert av.aluno == aluno
    assert av.professor == professor
    assert av.nota_b1 == 8.0
    assert av.nota_b2 == 7.5
    assert av.faltas == 2
    assert av.status == "Aprovado"
    assert av.media == 7.75

def test_read_avaliacao(aluno_professor_mock):
    aluno, professor = aluno_professor_mock
    av = AvaliacaoMock(aluno, professor, 6.0, 7.0, 1)
    av.save()
    found = AvaliacaoMock.get(av.id)
    assert found.nota_b1 == 6.0
    assert found.nota_b2 == 7.0
    assert found.faltas == 1

def test_update_avaliacao(aluno_professor_mock):
    aluno, professor = aluno_professor_mock
    av = AvaliacaoMock(aluno, professor, 5.0, 5.0, 3)
    av.save()
    # UPDATE
    av.nota_b1 = 7.0
    av.nota_b2 = 8.0
    av.faltas = 2
    av.media = (av.nota_b1 + av.nota_b2)/2
    av.status = av.calcular_status()
    assert av.nota_b1 == 7.0
    assert av.nota_b2 == 8.0
    assert av.faltas == 2
    assert av.media == 7.5
    assert av.status == "Aprovado"

def test_delete_avaliacao(aluno_professor_mock):
    aluno, professor = aluno_professor_mock
    av = AvaliacaoMock(aluno, professor, 9.0, 9.5, 0)
    av.save()
    av_id = av.id
    av.delete()
    with pytest.raises(ValueError):
        AvaliacaoMock.get(av_id)
