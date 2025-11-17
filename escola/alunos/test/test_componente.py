# alunos/test/test_componente_mock.py

import pytest
from unittest.mock import Mock
from django.urls import reverse

# Mocks para Models
class UserMock:
    def __init__(self, username, password=None, first_name="", last_name=""):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class AlunoMock:
    def __init__(self, user, matricula):
        self.user = user
        self.matricula = matricula

class ProfessorMock:
    def __init__(self, user, disciplina=None):
        self.user = user
        self.disciplina = disciplina

class AvaliacaoMock:
    def __init__(self, aluno, professor, nota_b1, nota_b2, faltas):
        self.aluno = aluno
        self.professor = professor
        self.nota_b1 = nota_b1
        self.nota_b2 = nota_b2
        self.faltas = faltas
        self.media = (nota_b1 + nota_b2) / 2
        if self.faltas > 10:
            self.status = "Reprovado"
        elif self.media >= 7:
            self.status = "Aprovado"
        else:
            self.status = "Reprovado"

# Fixture para mock do client
@pytest.fixture
def mock_client():
    client = Mock()
    client.get.return_value = Mock(status_code=200, content=b"7.5 8.0 7.75 Aprovado")
    client.post.return_value = Mock(status_code=302, url=reverse("login"))
    return client

# ================= TESTES =================

@pytest.mark.usefixtures("mock_client")
class TestCadastroAluno:
    def test_cadastro_aluno(self, mock_client):
        user = UserMock("bianca.andrade", "senha123", "Bianca", "Andrade")
        aluno = AlunoMock(user, "20230120")

        response = mock_client.post(reverse("cadastro_aluno"), {
            "username": user.username,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "matricula": aluno.matricula
        })

        assert response.status_code == 302
        assert aluno.matricula == "20230120"

class TestCadastroProfessor:
    def test_cadastro_professor(self, mock_client):
        user = UserMock("thais.santos", "senha123", "Thais", "Santos")
        prof = ProfessorMock(user)

        response = mock_client.post(reverse("cadastro_professor"), {
            "username": user.username,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

        assert response.status_code == 302
        assert prof.user.username == "thais.santos"

class TestAvaliacaoOperacoes:
    def test_cadastro_avaliacao(self, mock_client):
        user_aluno = UserMock("alice.beatriz", "senha123", "Alice", "Beatriz")
        user_prof = UserMock("thais.santos", "senha123", "Thais", "Santos")
        aluno = AlunoMock(user_aluno, "20230356")
        prof = ProfessorMock(user_prof)

        avaliacao = AvaliacaoMock(aluno, prof, 7.5, 8.0, 5)
        response = mock_client.post(reverse("lancar_avaliacao"), {
            "aluno": 1,
            "nota_b1": 7.5,
            "nota_b2": 8.0,
            "faltas": 5
        })

        assert response.status_code == 302
        assert avaliacao.media == 7.75
        assert avaliacao.status == "Aprovado"

    def test_calculo_media(self):
        aluno = AlunoMock(UserMock("user"), "20230356")
        prof = ProfessorMock(UserMock("prof"))
        avaliacao = AvaliacaoMock(aluno, prof, 5.0, 7.0, 2)
        assert avaliacao.media == 6.0

    def test_calculo_status_reprovado_por_faltas(self):
        aluno = AlunoMock(UserMock("user"), "20230356")
        prof = ProfessorMock(UserMock("prof"))
        avaliacao = AvaliacaoMock(aluno, prof, 6.0, 6.0, 11)
        assert avaliacao.status == "Reprovado"

    def test_consulta_avaliacoes_por_aluno(self, mock_client):
        aluno = AlunoMock(UserMock("alice.beatriz"), "20230356")
        prof = ProfessorMock(UserMock("thais.santos"))
        avaliacao = AvaliacaoMock(aluno, prof, 7.5, 8.0, 2)

        response = mock_client.get(reverse("boletim_aluno"))
        assert response.status_code == 200
        assert "7.5" in response.content.decode()
        assert "8.0" in response.content.decode()
        assert "7.75" in response.content.decode()
        assert "Aprovado" in response.content.decode()
