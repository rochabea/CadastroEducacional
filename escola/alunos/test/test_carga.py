# alunos/test/test_carga_mock.py

from locust import User, task, between
from unittest.mock import Mock
import re

# ===================== TESTE DE CARGA SIMULADO =====================

class MockResponse:
    def __init__(self, text="", status_code=200):
        self.text = text
        self.status_code = status_code

class MockClient:
    def get(self, url, **kwargs):
        print(f"GET mock {url}")
        # retorna conteúdo simulado
        return MockResponse(
            text='<input type="hidden" name="csrfmiddlewaretoken" value="token123">'
        )

    def post(self, url, data=None, headers=None, **kwargs):
        print(f"POST mock {url} with data {data}")
        return MockResponse(status_code=302)  # simula redirecionamento após login

# ===================== USUARIO ALUNO MOCK =====================

class UsuarioAlunoMock(User):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MockClient()
        self.csrf_token = None
        self.on_start()

    def on_start(self):
        response = self.client.get("/login/")
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', response.text)
        if match:
            self.csrf_token = match.group(1)
            print(f"CSRF token encontrado: {self.csrf_token}")
        else:
            print("CSRF token não encontrado!")
            return

        login_response = self.client.post(
            "/login/",
            data={
                "username": "alice.beatriz",
                "password": "senha123",
                "csrfmiddlewaretoken": self.csrf_token
            },
            headers={"Referer": "http://127.0.0.1:8000/login/"},
        )
        if login_response.status_code in [200, 302]:
            print("Login mock realizado com sucesso!")
        else:
            print(f"Falha no login mock: {login_response.status_code}")

    # ===================== Páginas do aluno =====================
    @task(3)
    def acessar_dashboard_aluno(self):
        resp = self.client.get("/dashboard/aluno/")
        print(f"Status mock /dashboard/aluno/: {resp.status_code}")

    @task(2)
    def acessar_quadro_horario(self):
        resp = self.client.get("/dashboard/quadro_horario_aluno/")
        print(f"Status mock /dashboard/quadro_horario_aluno/: {resp.status_code}")

    @task(2)
    def acessar_feedbacks(self):
        resp = self.client.get("/aluno/feedbacks/")
        print(f"Status mock /aluno/feedbacks/: {resp.status_code}")

    @task(1)
    def acessar_presenca_alunos(self):
        resp = self.client.get("/dashboard/presenca_alunos/")
        print(f"Status mock /dashboard/presenca_alunos/: {resp.status_code}")
