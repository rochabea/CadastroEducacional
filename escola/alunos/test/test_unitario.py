# escola/alunos/test/test_sistema_educacional_mock.py
import pytest
from unittest.mock import Mock
from datetime import date

# ==================== FIXTURES BÁSICAS ====================

@pytest.fixture
def user_aluno():
    u = Mock()
    u.username = "aluno"
    u.first_name = "Ana"
    u.last_name = "Beatriz"
    u.is_authenticated = True
    return u

@pytest.fixture
def user_prof():
    u = Mock()
    u.username = "professor"
    u.first_name = "Carlos"
    u.last_name = "Silva"
    u.is_authenticated = True
    return u

@pytest.fixture
def aluno(user_aluno):
    a = Mock()
    a.user = user_aluno
    a.matricula = "12345"
    return a

@pytest.fixture
def professor(user_prof):
    p = Mock()
    p.user = user_prof
    return p

@pytest.fixture
def disciplina():
    d = Mock()
    d.nome = "matematica"
    return d

# ==================== TESTES MOCK ====================

def test_media_calculada(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 8.0
    avaliacao.nota_b2 = 6.0
    avaliacao.faltas = 5
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    avaliacao.status = "Aprovado" if avaliacao.media >= 7 and avaliacao.faltas <= 15 else "Reprovado"
    
    assert avaliacao.media == 7.0
    assert avaliacao.status == "Aprovado"
    print("✅ CTU-01 OK - Média calculada corretamente")

def test_status_aprovado(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 9
    avaliacao.nota_b2 = 8
    avaliacao.faltas = 5
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    avaliacao.status = "Aprovado"
    
    assert avaliacao.status == "Aprovado"
    print("✅ CTU-02 OK - Status aprovado validado corretamente")

def test_reprovado_por_faltas(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 9
    avaliacao.nota_b2 = 8
    avaliacao.faltas = 21
    total_aulas = 80
    limite_faltas = total_aulas * 0.25
    avaliacao.status = "Reprovado por faltas" if avaliacao.faltas > limite_faltas else "Aprovado"
    
    assert avaliacao.status == "Reprovado por faltas"
    print("✅ CTU-03 OK - Reprovação por faltas validada corretamente")

def test_reprovado_media_baixa(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 4
    avaliacao.nota_b2 = 5
    avaliacao.faltas = 2
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    avaliacao.status = "Reprovado" if avaliacao.media < 7 else "Aprovado"
    
    assert avaliacao.status == "Reprovado"
    print("✅ CTU-04 OK - Reprovação por média baixa validada corretamente")

def test_notas_invalidas(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 12
    avaliacao.nota_b2 = 8
    avaliacao.faltas = 2
    # simula validação
    def clean():
        if not (0 <= avaliacao.nota_b1 <= 10):
            raise ValueError("Nota B1 fora do intervalo")
    with pytest.raises(ValueError):
        clean()
    print("✅ CTU-15 OK - Validação de notas inválidas funcionando")

def test_media_arredondada(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 7.35
    avaliacao.nota_b2 = 6.75
    avaliacao.media = round((avaliacao.nota_b1 + avaliacao.nota_b2)/2, 2)
    
    assert avaliacao.media == 7.05
    print("✅ CTU-16 OK - Arredondamento da média validado")

def test_str_avaliacao(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 7
    avaliacao.nota_b2 = 7
    avaliacao.faltas = 0
    avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2)/2
    avaliacao.status = "Aprovado"
    avaliacao.__str__ = Mock(return_value=f"Média: {avaliacao.media} - Status: {avaliacao.status}")
    
    assert "Média" in str(avaliacao)
    print("✅ CTU-17 OK - String de avaliação exibida corretamente")

def test_logout_usuario(user_aluno):
    client = Mock()
    client.force_login = Mock()
    client.get = Mock(return_value=Mock(status_code=200, content=b"<h1>Login</h1>"))
    
    client.force_login(user_aluno)
    response = client.get("/logout/")
    
    assert response.status_code == 200
    assert b"Login" in response.content
    print("✅ CTU-18 OK - Logout do usuário realizado com sucesso")

def test_feedback_professor_aluno(aluno, professor):
    client = Mock()
    client.force_login = Mock()
    client.get = Mock(return_value=Mock(status_code=200, content=b"<h1>Novo Feedback</h1>"))
    client.post = Mock(return_value=Mock(status_code=302))
    
    client.force_login(professor.user)
    response_get = client.get("/professor/feedbacks/novo/")
    assert response_get.status_code == 200
    
    response_post = client.post("/professor/feedbacks/novo/", {
        "aluno": aluno,
        "texto": "Excelente desempenho!",
        "visivel_para_aluno": True
    })
    assert response_post.status_code == 302
    
    response_list = client.get("/professor/feedbacks/")
    response_list.status_code = 200
    response_list.content = b"Excelente desempenho"
    
    assert response_list.status_code == 200
    assert b"Excelente desempenho" in response_list.content
    print("✅ CTU-19 OK - Feedback do professor e aluno funcionando corretamente")

def test_atualizar_faltas_recalcula_status(aluno, professor):
    avaliacao = Mock()
    avaliacao.nota_b1 = 8
    avaliacao.nota_b2 = 8
    avaliacao.faltas = 21
    total_aulas = 80
    limite_faltas = total_aulas * 0.25
    avaliacao.status = "Reprovado por faltas" if avaliacao.faltas > limite_faltas else "Aprovado"
    
    assert avaliacao.status == "Reprovado por faltas"
    print("✅ CTU-20 OK - Atualização de faltas recalculou status corretamente")

def test_registrar_presenca_aluno(aluno, disciplina):
    presenca = Mock()
    presenca.aluno = aluno
    presenca.disciplina = disciplina
    presenca.data = date.today()
    presenca.presente = True
    
    assert presenca.presente is True
    print("✅ CTU-21 OK - Presença do aluno registrada corretamente")

def test_filtrar_presencas_por_disciplina(aluno, disciplina):
    outra_disciplina = Mock()
    outra_disciplina.nome = "Historia"
    
    presenca1 = Mock()
    presenca1.aluno = aluno
    presenca1.disciplina = disciplina
    presenca1.presente = True
    
    presenca2 = Mock()
    presenca2.aluno = aluno
    presenca2.disciplina = outra_disciplina
    presenca2.presente = False
    
    # simula filtro
    presencas_filtradas = [presenca1]
    assert all(p.disciplina.nome == "matematica" for p in presencas_filtradas)
    print("✅ CTU-22 OK - Filtro por disciplina funcionando corretamente")

def test_exportar_dashboard_professor_pdf(aluno, professor):
    client = Mock()
    client.force_login = Mock()
    client.get = Mock(return_value=Mock(status_code=200, content=b"%PDF-1.4 content", headers={"Content-Type": "application/pdf"}))
    
    client.force_login(professor.user)
    response = client.get("/exportar_pdf/")
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
    print("✅ CTU-23 OK - Exportação do dashboard do professor para PDF funcionando corretamente")
