# escola/alunos/test/test_consultas_integration.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

URL_QUADRO_HORARIO = "quadro_aluno_view"
URL_FEEDBACK_LIST  = "aluno-meus-feedbacks"
URL_PRESENCA_LIST  = "presenca_alunos"

# Adicione a fixture aqui
@pytest.fixture
def user_aluno(db):
    """Cria um usuário aluno para testes"""
    user = User.objects.create_user(
        username="tio123",
        password="SenhaForte123!",
        email="tio123@example.com"
    )
    return user

@pytest.mark.django_db
def test_CT08_consulta_quadro_horario(client, user_aluno):
    client.force_login(user_aluno)  # Melhor que login() em testes
    resp = client.get(reverse(URL_QUADRO_HORARIO), follow=True)
    assert resp.status_code == 200
    html = resp.content.decode().lower()
    assert any(k in html for k in ["aula", "horário", "turma", "quadro"])

@pytest.mark.django_db
def test_CT09_acesso_lista_feedbacks(client, user_aluno):
    client.force_login(user_aluno)
    resp = client.get(reverse(URL_FEEDBACK_LIST))
    assert resp.status_code == 200
    html = resp.content.decode().lower()
    assert any(k in html for k in ["feedback", "coment", "avalia"])

@pytest.mark.django_db
def test_CT10_consulta_presenca(client, user_aluno):
    client.force_login(user_aluno)
    resp = client.get(reverse(URL_PRESENCA_LIST))
    assert resp.status_code == 200
    html = resp.content.decode().lower()
    assert any(k in html for k in ["presen", "aula", "aluno"])