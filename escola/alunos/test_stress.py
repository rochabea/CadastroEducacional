from locust import HttpUser, task, between
import re

class UsuarioAluno(HttpUser):
    wait_time = between(0.5, 1)

    def on_start(self):
        # Acessa a página de login para obter o CSRF token
        response = self.client.get("/login/")
        if response.status_code != 200:
            print(f"Erro ao carregar login: {response.status_code}")
            return

        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', response.text)
        if not match:
            print("CSRF token não encontrado na página de login.")
            return
        csrf_token = match.group(1)

        # Realiza o login
        login_response = self.client.post(
            "/login/",
            data={
                "username": "alice.beatriz",
                "password": "senha123",
                "csrfmiddlewaretoken": csrf_token,
            },
            headers={"Referer": "http://127.0.0.1:8000/login/"},
            allow_redirects=True,  # permite seguir redirecionamento automático
        )

        if login_response.status_code in [200, 302]:
            print("Login realizado com sucesso.")
        else:
            print(f"Falha no login - status: {login_response.status_code}")
            print(login_response.text[:300])

    @task(3)
    def acessar_boletim(self):
        response = self.client.get("/aluno/boletim/")
        if response.status_code == 200:
            print("Acessou boletim.")
        else:
            print(f"Falha ao acessar boletim: {response.status_code}")

    @task(1)
    def acessar_dashboard_aluno(self):
        response = self.client.get("/dashboard/aluno/")
        if response.status_code == 200:
            print("Acessou dashboard.")
        else:
            print(f"Falha ao acessar dashboard: {response.status_code}")
