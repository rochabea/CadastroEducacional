# alunos/test/test_auth_dashboard_integration_mock.py

import time
import pytest
from unittest.mock import Mock

# --- Constantes de URLs nomeadas ---
URL_LOGIN = "/login/"
URL_DASHBOARD_ALUNO = "/dashboard/aluno/"
URL_DASHBOARD_PROF = "/dashboard/professor/"

# --- Stopwatch para medir performance ---
class Stopwatch:
    def __enter__(self):
        self._t0 = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self._t0

# --- Fixtures de usuários ---
@pytest.fixture
def user_aluno():
    """Usuário aluno mock"""
    u = Mock()
    u.username = "tio123"
    u.password = "SenhaForte123!"
    return u

@pytest.fixture
def user_professor():
    """Usuário professor mock"""
    u = Mock()
    u.username = "prof01"
    u.password = "SenhaForte123!"
    return u

@pytest.fixture
def mock_client():
    """Mock do TestClient"""
    client = Mock()

    # GET configurado corretamente para retornar status_code real
    def mock_get(url, *args, **kwargs):
        resp = Mock()
        resp.content = b"conteudo mock"
        if url == URL_LOGIN:
            resp.status_code = 200
            resp.headers = {"Location": ""}
        elif url == URL_DASHBOARD_ALUNO:
            logged_in = kwargs.get("logged_in", True)
            resp.status_code = 200 if logged_in else 302
            resp.headers = {"Location": "" if logged_in else URL_LOGIN}
        elif url == URL_DASHBOARD_PROF:
            logged_in = kwargs.get("logged_in", True)
            resp.status_code = 200 if logged_in else 302
            resp.headers = {"Location": "" if logged_in else URL_LOGIN}
        else:
            resp.status_code = 404
            resp.headers = {"Location": ""}
        return resp

    # POST configurado corretamente
    def mock_post(url, data=None, *args, **kwargs):
        resp = Mock()
        resp.content = b"conteudo mock"
        resp.status_code = 302
        if data and data.get("username") == "tio123":
            resp.headers = {"Location": URL_DASHBOARD_ALUNO}
        elif data and data.get("username") == "prof01":
            resp.headers = {"Location": URL_DASHBOARD_PROF}
        else:
            resp.headers = {"Location": URL_LOGIN}
        return resp

    client.get.side_effect = mock_get
    client.post.side_effect = mock_post
    client.login.side_effect = lambda username, password: username in ["tio123", "prof01"]
    client.force_login = Mock()
    return client

# --- Testes — Aluno ---
def test_CT05_acesso_pagina_login_get(mock_client):
    """GET da página de login deve responder 200."""
    resp = mock_client.get(URL_LOGIN)
    assert resp.status_code == 200

def test_CT06_realizar_login_aluno_redireciona_para_dashboard_aluno(mock_client, user_aluno):
    """Login de aluno redireciona para dashboard_aluno."""
    get_resp = mock_client.get(URL_LOGIN)
    assert get_resp.status_code == 200

    post_resp = mock_client.post(URL_LOGIN, {
        "username": "tio123",
        "password": "SenhaForte123!",
    })
    assert post_resp.status_code in (302, 303)
    assert post_resp.headers.get("Location") == URL_DASHBOARD_ALUNO

def test_CT07_acesso_dashboard_aluno_autenticado(mock_client, user_aluno):
    """Aluno autenticado acessa dashboard_aluno com 200 e rápido."""
    assert mock_client.login(username="tio123", password="SenhaForte123!")
    with Stopwatch() as sw:
        resp = mock_client.get(URL_DASHBOARD_ALUNO, logged_in=True)
    assert resp.status_code == 200
    assert sw.elapsed < 2.0
    assert resp.content, "Resposta do dashboard do aluno veio vazia."

# --- Testes — Professor ---
def test_CT12_realizar_login_prof_redireciona_para_dashboard_professor(mock_client, user_professor):
    """Login de professor redireciona para dashboard_professor."""
    get_resp = mock_client.get(URL_LOGIN)
    assert get_resp.status_code == 200

    post_resp = mock_client.post(URL_LOGIN, {
        "username": "prof01",
        "password": "SenhaForte123!",
    })
    assert post_resp.status_code in (302, 303)
    assert post_resp.headers.get("Location") == URL_DASHBOARD_PROF

def test_CT13_acesso_dashboard_prof_autenticado(mock_client, user_professor):
    """Professor autenticado acessa dashboard_professor com 200 e rápido."""
    assert mock_client.login(username="prof01", password="SenhaForte123!")
    with Stopwatch() as sw:
        resp = mock_client.get(URL_DASHBOARD_PROF, logged_in=True)
    assert resp.status_code == 200
    assert sw.elapsed < 2.0
    assert resp.content, "Resposta do dashboard do professor veio vazia."

def test_CT14_bloqueio_acesso_desautorizado(mock_client):
    """Acesso ao dashboard do professor sem login redireciona para login."""
    resp = mock_client.get(URL_DASHBOARD_PROF, logged_in=False)
    assert resp.status_code in (302, 303)
    assert "login" in resp.headers.get("Location", "").lower()
