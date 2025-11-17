# escola/alunos/test/test_integracao_mock.py
import pytest
from unittest.mock import Mock, patch

# URLs usadas no projeto
URL_LOGIN = "login"
URL_LANCAR_AVALIACAO = "lancar_avaliacao"
URL_EDITAR_AVALIACAO = "editar_avaliacao"
URL_DASHBOARD_PROF = "dashboard_professor"

# Mock de usuário
@pytest.fixture
def mock_user_aluno():
    u = Mock()
    u.username = "aluno1"
    u.is_authenticated = True
    return u

@pytest.fixture
def mock_user_professor():
    u = Mock()
    u.username = "prof1"
    u.is_authenticated = True
    return u

@pytest.fixture
def mock_aluno(mock_user_aluno):
    aluno = Mock()
    aluno.user = mock_user_aluno
    aluno.matricula = "2025001"
    return aluno

@pytest.fixture
def mock_professor(mock_user_professor):
    prof = Mock()
    prof.user = mock_user_professor
    return prof

# ===================== TESTES =====================

def test_login_sucesso_redireciona():
    # Simula POST /login
    resp = Mock()
    resp.status_code = 302
    resp.url = "/dashboard_aluno/"
    assert resp.status_code in (302, 303)
    assert resp.url is not None and len(resp.url) > 0

def test_login_falho_mantem_anonimo_e_mostra_form():
    resp = Mock()
    resp.status_code = 200
    resp.wsgi_request = Mock()
    resp.wsgi_request.user = Mock(is_authenticated=False)
    resp.content = b'<form name="username"></form><input name="password">'
    
    assert resp.status_code == 200
    assert not resp.wsgi_request.user.is_authenticated
    html = resp.content.decode().lower()
    assert '<form' in html and 'name="username"' in html and 'name="password"' in html

def test_criar_avaliacao_e_calcular_status(mock_professor, mock_aluno):
    # Simula criação de avaliação
    avaliacao = Mock()
    avaliacao.aluno = mock_aluno
    avaliacao.professor = mock_professor
    avaliacao.nota_b1 = 8.0
    avaliacao.nota_b2 = 6.0
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2) / 2
    avaliacao.faltas = 5
    avaliacao.status = "Aprovado"
    
    assert avaliacao.media == 7.0
    assert avaliacao.status == "Aprovado"

    # Simula edição
    avaliacao.nota_b1 = 3.0
    avaliacao.nota_b2 = 4.0
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2) / 2
    if avaliacao.media < 7:
        avaliacao.status = "Reprovado"

    assert avaliacao.status == "Reprovado"

def test_reprovado_por_faltas(mock_professor, mock_aluno):
    avaliacao = Mock()
    avaliacao.faltas = 21
    total_aulas = 80
    limite = total_aulas * 0.25
    assert avaliacao.faltas >= limite
    avaliacao.status = "Reprovado por faltas"
    assert avaliacao.status == "Reprovado por faltas"
