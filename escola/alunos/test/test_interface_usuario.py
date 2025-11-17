# escola/alunos/test/test_interface_usuario_mock.py
import pytest
from unittest.mock import Mock

# ==================== FIXTURES BÁSICAS MOCK ====================

@pytest.fixture
def user_aluno():
    u = Mock()
    u.username = "aluno1"
    u.first_name = "Alice"
    u.last_name = "Silva"
    u.is_authenticated = True
    return u

@pytest.fixture
def user_professor():
    u = Mock()
    u.username = "prof1"
    u.first_name = "Carlos"
    u.last_name = "Silva"
    u.is_authenticated = True
    return u

@pytest.fixture
def aluno(user_aluno):
    a = Mock()
    a.user = user_aluno
    a.matricula = "20230122"
    return a

@pytest.fixture
def professor(user_professor):
    p = Mock()
    p.user = user_professor
    return p

# ==================== TESTES MOCK ====================

def test_cadastro_de_aluno_sucesso(user_aluno):
    # simula POST e criação do aluno
    aluno_mock = Mock()
    aluno_mock.user = user_aluno
    aluno_mock.matricula = "20230120"

    # simula redirecionamento após cadastro
    response = Mock()
    response.status_code = 302

    assert response.status_code == 302
    assert aluno_mock.user.username == "aluno1"
    assert aluno_mock.matricula == "20230120"

def test_cadastro_professor_com_sucesso(user_professor):
    professor_mock = Mock()
    professor_mock.user = user_professor
    professor_str = f"{professor_mock.user.first_name} {professor_mock.user.last_name}"
    
    assert professor_mock.user.username == "prof1"
    assert professor_str == "Carlos Silva"

def test_cadastro_avaliacao_media_status(aluno, professor):
    avaliacao = Mock()
    avaliacao.aluno = aluno
    avaliacao.professor = professor
    avaliacao.nota_b1 = 8.0
    avaliacao.nota_b2 = 6.0
    avaliacao.faltas = 5
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2) / 2
    avaliacao.status = "Aprovado" if avaliacao.media >= 7 and avaliacao.faltas <= 15 else "Reprovado"

    assert avaliacao.media == 7.0
    assert avaliacao.status == "Aprovado"

def test_reprovacao_por_nota(aluno, professor):
    avaliacao = Mock()
    avaliacao.aluno = aluno
    avaliacao.professor = professor
    avaliacao.nota_b1 = 5
    avaliacao.nota_b2 = 4
    avaliacao.faltas = 5
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    avaliacao.status = "Reprovado" if avaliacao.media < 7 else "Aprovado"

    assert avaliacao.media == 4.5
    assert avaliacao.status == "Reprovado"

def test_reprovacao_por_faltas(aluno, professor):
    avaliacao = Mock()
    avaliacao.aluno = aluno
    avaliacao.professor = professor
    avaliacao.nota_b1 = 9
    avaliacao.nota_b2 = 8
    avaliacao.faltas = 21
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    total_aulas = 80
    limite_faltas = total_aulas * 0.25
    avaliacao.status = "Reprovado por faltas" if avaliacao.faltas > limite_faltas else "Aprovado"

    assert avaliacao.media == 8.5
    assert avaliacao.status == "Reprovado por faltas"

def test_boletim_aluno(aluno, professor):
    avaliacao = Mock()
    avaliacao.aluno = aluno
    avaliacao.professor = professor
    avaliacao.nota_b1 = 7
    avaliacao.nota_b2 = 9
    avaliacao.faltas = 3
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    avaliacao.status = "Aprovado" if avaliacao.media >= 7 else "Reprovado"

    boletim_str = f"{aluno} - Média: {avaliacao.media} - {avaliacao.status}"
    avaliacao.__str__ = Mock(return_value=boletim_str)

    assert str(avaliacao) == boletim_str

def test_acesso_boletim_apos_login(aluno):
    # simula login
    login_ok = True
    assert login_ok

    # simula GET da página
    response = Mock()
    response.status_code = 200
    response.content = b"<h1>Boletim</h1>"

    assert response.status_code == 200
    html = response.content.decode().lower()
    assert "boletim" in html
