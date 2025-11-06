# escola/alunos/test/test_consultas_integration.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

URL_QUADRO_HORARIO = "quadro_aluno_view"
URL_FEEDBACK_LIST  = "aluno-meus-feedbacks"
URL_PRESENCA_LIST  = "presenca_alunos"

@pytest.fixture
def contexto_aluno_logado(db, client):
    """
    Cria:
      - User (tio123) e o respectivo Aluno (obrigatório para suas views)
      - Professor e User do professor (para criar Feedback)
      - Disciplina, vínculo do aluno e uma Presenca
      - Um Feedback visível para o aluno
    E já autentica o aluno no client.
    """
    User = get_user_model()

    # Usuário/aluno
    u = User.objects.create_user(
        username="tio123",
        password="SenhaForte123!",
        email="tio123@example.com",
        first_name="Aluno",
        last_name="Teste",
    )

    from alunos.models import Aluno, Professor, Disciplina, Presenca, Feedback
    aluno = Aluno.objects.create(user=u)

    # Professor (necessário para Feedbacks)
    prof_user = User.objects.create_user(
        username="prof01",
        password="SenhaForte123!",
        email="prof01@example.com",
        first_name="Profe",
        last_name="Teste",
    )
    professor = Professor.objects.create(user=prof_user)

    # Disciplina e presença (para a tela de presenças renderizar algo)
    disc = Disciplina.objects.create(nome="Matemática")
    aluno.disciplinas.add(disc)
    Presenca.objects.create(aluno=aluno, disciplina=disc, presente=False)

    # Feedback visível para o aluno (para a lista não vir vazia)
    Feedback.objects.create(
        aluno=aluno,
        professor=professor,
        texto="Seu desempenho melhorou!",
        visivel_para_aluno=True,
    )

    client.force_login(u)
    return {"user": u, "aluno": aluno, "professor": professor, "disciplina": disc}

@pytest.mark.django_db
def test_CT08_consulta_quadro_horario(client, contexto_aluno_logado):
    resp = client.get(reverse(URL_QUADRO_HORARIO), follow=True)
    assert resp.status_code == 200
    html = resp.content.decode().lower()
    # seja tolerante com acento e variações
    assert any(k in html for k in ["aula", "horário", "horario", "turma", "quadro"])

@pytest.mark.django_db
def test_CT09_acesso_lista_feedbacks(client, contexto_aluno_logado):
    resp = client.get(reverse(URL_FEEDBACK_LIST))
    assert resp.status_code == 200
    html = resp.content.decode().lower()
    # tolerante a plural/singular e acentos
    assert any(k in html for k in ["feedback", "coment", "avalia"])

@pytest.mark.django_db
def test_CT10_consulta_presenca(client, contexto_aluno_logado):
    resp = client.get(reverse(URL_PRESENCA_LIST))
    assert resp.status_code == 200
    html = resp.content.decode().lower()
    assert any(k in html for k in ["presen", "aula", "aluno"])
