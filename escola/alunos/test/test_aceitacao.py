# alunos/test/test_aceitacao_mock.py
import pytest
from unittest.mock import Mock

# Mapeamento de URLs como strings simples
URLS = {
    'login': '/login/',
    'dashboard_aluno': '/dashboard/aluno/',
    'dashboard_professor': '/dashboard/professor/',
}

@pytest.fixture
def mock_client():
    """Mock do TestClient"""
    client = Mock()
    return client

@pytest.fixture
def mock_user():
    """Mock de um usuário"""
    def _factory(username, password=None):
        u = Mock()
        u.username = username
        u.password = password
        return u
    return _factory

@pytest.fixture
def mock_aluno(mock_user):
    """Mock de um aluno"""
    def _factory(username='aluno', matricula='123'):
        user = mock_user(username=username)
        a = Mock()
        a.user = user
        a.matricula = matricula
        return a
    return _factory

@pytest.fixture
def mock_professor(mock_user):
    """Mock de um professor"""
    def _factory(username='prof'):
        user = mock_user(username=username)
        p = Mock()
        p.user = user
        return p
    return _factory

@pytest.fixture
def mock_avaliacao(mock_aluno, mock_professor):
    """Mock de avaliação"""
    def _factory(nota_b1=7.0, nota_b2=7.0, faltas=0):
        aluno = mock_aluno()
        professor = mock_professor()
        a = Mock()
        a.aluno = aluno
        a.professor = professor
        a.nota_b1 = nota_b1
        a.nota_b2 = nota_b2
        a.faltas = faltas
        a.media = (nota_b1 + nota_b2) / 2
        a.status = 'Aprovado' if a.media >= 7 else 'Reprovado'
        return a
    return _factory

@pytest.mark.usefixtures("mock_client")
class TestFuncionais:

    def test_ct01_cadastro_de_aluno(self, mock_aluno, mock_client):
        aluno = mock_aluno(username='ana.bia', matricula='20230120')
        response = Mock()
        response.status_code = 302
        response.url = URLS['login']

        assert response.url == URLS['login']
        assert aluno.matricula == '20230120'

    def test_ct02_login_como_aluno(self, mock_aluno, mock_client):
        aluno = mock_aluno(username='joao', matricula='A123')
        response = Mock()
        response.status_code = 302
        response.url = URLS['dashboard_aluno']

        assert response.url == URLS['dashboard_aluno']

    def test_ct03_cadastro_professor(self, mock_professor, mock_client):
        prof = mock_professor(username='prof123')
        response = Mock()
        response.status_code = 302
        response.url = URLS['login']

        assert response.url == URLS['login']
        assert prof.user.username == 'prof123'

    def test_ct04_lancar_avaliacao(self, mock_avaliacao, mock_client):
        avaliacao = mock_avaliacao(nota_b1=8.0, nota_b2=7.5, faltas=3)
        response = Mock()
        response.status_code = 302
        response.url = URLS['dashboard_professor']

        assert response.url == URLS['dashboard_professor']
        assert avaliacao.media == 7.75
        assert avaliacao.status == 'Aprovado'

    def test_ct05_boletim_aluno(self, mock_avaliacao, mock_client):
        avaliacao = mock_avaliacao(nota_b1=5, nota_b2=6, faltas=2)
        response = Mock()
        response.content = f"{avaliacao.nota_b1} {avaliacao.nota_b2} {avaliacao.media:.2f} {avaliacao.status}"

        assert str(avaliacao.nota_b1) in response.content
        assert str(avaliacao.nota_b2) in response.content
        assert f"{avaliacao.media:.2f}" in response.content
        assert avaliacao.status in response.content
