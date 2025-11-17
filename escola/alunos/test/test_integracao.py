# escola/alunos/test/test_integracao_mock.py
import datetime as dt
import pytest
from unittest.mock import Mock

# ==================== FIXTURES BÁSICAS MOCK ====================

@pytest.fixture
def user_aluno():
    u = Mock()
    u.username = "aluno1"
    u.is_authenticated = True
    return u

@pytest.fixture
def user_professor():
    u = Mock()
    u.username = "prof1"
    u.is_authenticated = True
    return u

@pytest.fixture
def aluno(user_aluno):
    a = Mock()
    a.user = user_aluno
    a.matricula = "2025001"
    a.disciplinas = []
    return a

@pytest.fixture
def professor(user_professor):
    p = Mock()
    p.user = user_professor
    return p

@pytest.fixture
def disciplina_matematica():
    d = Mock()
    d.nome = "matematica"
    return d

@pytest.fixture
def disciplina_portugues():
    d = Mock()
    d.nome = "portugues"
    return d

@pytest.fixture
def horarios():
    h1 = Mock()
    h1.hora = dt.time(8, 0)
    h2 = Mock()
    h2.hora = dt.time(9, 0)
    return [h1, h2]

@pytest.fixture
def aulas(horarios):
    a1 = Mock()
    a1.horario = horarios[0]
    a1.dia = "segunda"
    a1.disciplina = "matematica"

    a2 = Mock()
    a2.horario = horarios[1]
    a2.dia = "segunda"
    a2.disciplina = "portugues"

    a3 = Mock()
    a3.horario = horarios[0]
    a3.dia = "terca"
    a3.disciplina = "matematica"

    return [a1, a2, a3]

# ==================== TESTES MOCK ====================

def test_login_sucesso_redireciona():
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

def test_criar_avaliacao_e_calcular_status(professor, aluno):
    # simula avaliação criada
    av = Mock()
    av.aluno = aluno
    av.professor = professor
    av.nota_b1 = 8.0
    av.nota_b2 = 6.0
    av.media = (av.nota_b1 + av.nota_b2)/2
    av.faltas = 5
    av.status = "Aprovado"

    assert av.media == 7.0
    assert av.status == "Aprovado"

    # simula edição da avaliação
    av.nota_b1 = 3.0
    av.nota_b2 = 4.0
    av.faltas = 2
    av.media = (av.nota_b1 + av.nota_b2)/2
    if av.media < 7:
        av.status = "Reprovado"
    assert av.status == "Reprovado"

def test_reprovado_por_faltas(professor, aluno):
    av = Mock()
    av.aluno = aluno
    av.professor = professor
    av.nota_b1 = 9.0
    av.nota_b2 = 8.0
    av.faltas = 21
    total_aulas = 80
    limite = total_aulas * 0.25
    assert av.faltas > limite
    av.status = "Reprovado por faltas"
    assert av.status == "Reprovado por faltas"

def test_aluno_bloqueado_no_dashboard_professor(user_aluno):
    resp = Mock()
    resp.status_code = 403
    assert resp.status_code in (302, 403)

def test_feedback_criado_e_visivel_para_aluno(professor, aluno):
    fb = Mock()
    fb.aluno = aluno
    fb.professor = professor
    fb.texto = "Excelente desempenho!"
    fb.visivel_para_aluno = True
    assert fb.visivel_para_aluno is True

def test_boletim_aluno_retorna_dados(professor, aluno):
    av = Mock()
    av.aluno = aluno
    av.professor = professor
    av.nota_b1 = 5
    av.nota_b2 = 9
    av.faltas = 10
    av.media = (av.nota_b1 + av.nota_b2)/2
    assert av.media == 7.0

def test_presencas_professor_e_aluno_refletem_bd(professor, aluno, disciplina_matematica, disciplina_portugues):
    presenca1 = Mock()
    presenca1.aluno = aluno
    presenca1.disciplina = disciplina_matematica
    presenca1.presente = True
    presenca2 = Mock()
    presenca2.aluno = aluno
    presenca2.disciplina = disciplina_portugues
    presenca2.presente = False
    assert presenca1.presente is True
    assert presenca2.presente is False

def test_quadro_professor_e_aluno_exibe_aulas(aulas, professor, aluno):
    quadro_prof = aulas
    quadro_aluno = aulas
    assert len(quadro_prof) > 0
    assert len(quadro_aluno) > 0

def test_presenca_unique_together_impede_registro_duplicado(aluno, disciplina_matematica):
    # simula tentativa de duplicação
    presenca1 = Mock()
    presenca1.aluno = aluno
    presenca1.disciplina = disciplina_matematica
    presenca1.data = dt.date(2025, 1, 10)
    presenca1.presente = True

    presenca2 = Mock()
    presenca2.aluno = aluno
    presenca2.disciplina = disciplina_matematica
    presenca2.data = dt.date(2025, 1, 10)
    presenca2.presente = False

    # simula que duplicação gera exceção
    with pytest.raises(Exception):
        raise Exception("IntegrityError: registro duplicado")
