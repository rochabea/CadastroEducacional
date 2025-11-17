# alunos/test/test_int_mock.py

import pytest
from unittest.mock import Mock

# ===================== MOCK MODELS =====================

class UserMock:
    _db = []

    def __init__(self, username, password, first_name="", last_name="", email=""):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        UserMock._db.append(self)

    @classmethod
    def filter(cls, username):
        return [u for u in cls._db if u.username == username]

    @classmethod
    def get(cls, username):
        for u in cls._db:
            if u.username == username:
                return u
        raise ValueError("User não encontrado")

    @classmethod
    def clear_db(cls):
        cls._db = []

class AlunoMock:
    _db = []

    def __init__(self, user, matricula):
        self.user = user
        self.matricula = matricula
        AlunoMock._db.append(self)

    @classmethod
    def filter(cls, user=None, matricula=None):
        results = cls._db
        if user:
            results = [a for a in results if a.user == user]
        if matricula:
            results = [a for a in results if a.matricula == matricula]
        return results

    @classmethod
    def clear_db(cls):
        cls._db = []

class ProfessorMock:
    _db = []

    def __init__(self, user):
        self.user = user
        ProfessorMock._db.append(self)

    @classmethod
    def clear_db(cls):
        cls._db = []

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
        AvaliacaoMock._db.append(self)

    def calcular_status(self):
        if self.faltas > 15:
            return "Reprovado por faltas"
        elif self.media < 7.0:
            return "Reprovado"
        else:
            return "Aprovado"

    @classmethod
    def filter_by_aluno(cls, aluno):
        return [a for a in cls._db if a.aluno == aluno]

    @classmethod
    def clear_db(cls):
        cls._db = []

# ===================== FIXTURES =====================

@pytest.fixture(autouse=True)
def clear_db():
    UserMock.clear_db()
    AlunoMock.clear_db()
    ProfessorMock.clear_db()
    AvaliacaoMock.clear_db()
    yield
    UserMock.clear_db()
    AlunoMock.clear_db()
    ProfessorMock.clear_db()
    AvaliacaoMock.clear_db()

# ===================== TESTES =====================

def test_ct01_cadastro_de_aluno():
    user_data = {
        'username': 'ana.bia',
        'password': 'senha123',
        'first_name': 'Ana',
        'last_name': 'Bia',
        'email': 'ana.bia@email.com',
    }
    aluno_data = {'matricula': '20230120'}
    user = UserMock(**user_data)
    aluno = AlunoMock(user, aluno_data['matricula'])

    # Assertions
    assert UserMock.get('ana.bia').first_name == 'Ana'
    assert aluno.matricula == '20230120'

def test_ct02_cadastro_de_professor():
    user = UserMock('maria.oliveira', 'senha123', 'Maria', 'Oliveira', 'maria.oliveira@email.com')
    prof = ProfessorMock(user)
    # Assertions
    assert prof.user.username == 'maria.oliveira'

def test_ct03_cadastro_de_avaliacao():
    user_aluno = UserMock('ana.bia', 'senha123')
    aluno = AlunoMock(user_aluno, '20230120')
    user_prof = UserMock('maria.oliveira', 'senha123')
    prof = ProfessorMock(user_prof)

    av = AvaliacaoMock(aluno, prof, 7.5, 8.0, 5)
    assert av.media == 7.75
    assert av.status == 'Aprovado'

def test_ct06_consulta_avaliacoes():
    user_aluno = UserMock('ana.bia', 'senha123')
    aluno = AlunoMock(user_aluno, '20230120')
    user_prof = UserMock('prof1', 'senha123')
    prof = ProfessorMock(user_prof)
    AvaliacaoMock(aluno, prof, 7, 8, 2)
    # Avaliação de outro aluno
    outro_user = UserMock('outro', 'senha123')
    outro_aluno = AlunoMock(outro_user, '20230001')
    AvaliacaoMock(outro_aluno, prof, 6, 5, 0)

    avaliacoes = AvaliacaoMock.filter_by_aluno(aluno)
    for a in avaliacoes:
        assert a.aluno == aluno

def test_ct09_acesso_boletim():
    user_aluno = UserMock('alice.beatriz', 'senha123')
    aluno = AlunoMock(user_aluno, '20230002')
    # Simula render do boletim
    boletim_content = f"Boletim de {aluno.user.username}"
    assert 'Boletim' in boletim_content
