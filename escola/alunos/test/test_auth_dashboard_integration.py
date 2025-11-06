import time
import pytest
from django.urls import reverse

URL_LOGIN = "login"
URL_DASHBOARD_ALUNO = "dashboard_aluno"
URL_DASHBOARD_PROF = "dashboard_professor"

class Stopwatch:
    def __enter__(self):
        self._t0 = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self._t0

# Fixtures

@pytest.fixture
def user_aluno(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username="tio123",
        password="SenhaForte123!",
        first_name="Aluno",
        last_name="Teste",
        email="aluno.teste@example.com",
    )

@pytest.fixture
def user_professor(db):
    from django.contrib.auth import get_user_model
    from alunos.models import Professor
    User = get_user_model()
    u = User.objects.create_user(
        username="prof01",
        password="SenhaForte123!",
        first_name="Profe",
        last_name="Teste",
        email="prof.teste@example.com",
    )
    # vincula o User a um Professor (dashboard_professor exige Professor.objects.get(user=request.user))
    Professor.objects.create(user=u)
    return u

# Testes — Aluno

@pytest.mark.django_db
def test_CT05_acesso_pagina_login_get(client):
    """GET da página de login deve responder 200."""
    resp = client.get(reverse(URL_LOGIN))
    assert resp.status_code == 200

@pytest.mark.django_db
def test_CT06_realizar_login_aluno_redireciona_para_dashboard_aluno(client, user_aluno):
    """
    Login de aluno deve redirecionar para dashboard do aluno.
    Sem tocar no conftest: garantimos aqui o vínculo User -> Aluno.
    """
    from alunos.models import Aluno
    from django.urls import reverse

    # garante o papel correto para o fluxo da view
    Aluno.objects.get_or_create(user=user_aluno)

    # GET exibe a página de login
    get_resp = client.get(reverse(URL_LOGIN))
    assert get_resp.status_code == 200

    # POST realiza o login (follow pra inspecionar Location do 302)
    post_resp = client.post(reverse(URL_LOGIN), {
        "username": "tio123",
        "password": "SenhaForte123!",
    })
    assert post_resp.status_code in (302, 303)

    # destino = dashboard_aluno
    location = post_resp.headers.get("Location", "")
    assert "/dashboard/aluno" in location or reverse(URL_DASHBOARD_ALUNO) in location


@pytest.mark.django_db
def test_CT07_acesso_dashboard_aluno_autenticado(client, user_aluno):
    """Sessão autenticada de aluno acessa dashboard rapidamente e recebe 200."""
    assert client.login(username="tio123", password="SenhaForte123!")
    with Stopwatch() as sw:
        resp = client.get(reverse(URL_DASHBOARD_ALUNO))
    assert resp.status_code == 200
    assert sw.elapsed < 2.0, f"Dashboard (aluno) demorou {sw.elapsed:.2f}s (limite < 2s)"
    assert resp.content, "Resposta do dashboard do aluno veio vazia."

# Testes — Professor

@pytest.mark.django_db
def test_CT08_realizar_login_prof_redireciona_para_dashboard_professor(client, user_professor):
    """Login de professor deve redirecionar para dashboard do professor."""
    # GET exibe login
    get_resp = client.get(reverse(URL_LOGIN))
    assert get_resp.status_code == 200

    # POST login
    post_resp = client.post(reverse(URL_LOGIN), {
        "username": "prof01",
        "password": "SenhaForte123!",
    })
    assert post_resp.status_code in (302, 303)

    # destino = dashboard_professor
    location = post_resp.headers.get("Location", "")
    assert "/dashboard/professor" in location or reverse(URL_DASHBOARD_PROF) in location

@pytest.mark.django_db
def test_CT09_acesso_dashboard_prof_autenticado(client, user_professor):
    """Sessão autenticada de professor acessa dashboard rapidamente e recebe 200."""
    assert client.login(username="prof01", password="SenhaForte123!")
    with Stopwatch() as sw:
        resp = client.get(reverse(URL_DASHBOARD_PROF))
    assert resp.status_code == 200
    assert sw.elapsed < 2.0, f"Dashboard (prof) demorou {sw.elapsed:.2f}s (limite < 2s)"
    assert resp.content, "Resposta do dashboard do professor veio vazia."

@pytest.mark.django_db
def test_CT10_dashboard_professor_sem_login_redireciona(client):
    """Acesso ao dashboard do professor sem autenticação deve redirecionar para login (middleware de auth)."""
    resp = client.get(reverse(URL_DASHBOARD_PROF))
    # por padrão, @login_required redireciona (302) para LOGIN_URL com ?next=...
    assert resp.status_code in (302, 303)
    assert "login" in resp.headers.get("Location", "").lower()
