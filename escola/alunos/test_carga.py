from locust import HttpUser, task, between
import re

class UsuarioAluno(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Primeiro pega a página de login para extrair o token CSRF
        response = self.client.get("/login/")
        csrf_token = re.search(
            r'name="csrfmiddlewaretoken" value="(.+?)"', response.text
        ).group(1)
        
        # Faz login enviando username, password e o token CSRF
        login_response = self.client.post(
            "/login/",
            data={
                "username": "alice.beatriz",
                "password": "senha123",
                "csrfmiddlewaretoken": csrf_token,
            },
            headers={"Referer": "http://127.0.0.1:8000/login/"},
            allow_redirects=True,
        )
        print(f"Login status: {login_response.status_code}")
        print(f"Login response URL: {login_response.url}")
        print(f"Cookies: {self.client.cookies.get_dict()}")

    # CT06 - Consulta de Avaliações por Aluno
    # Visualização das próprias avaliações
@task(2)
def consultar_avaliacoes(self):
    response = self.client.get("/avaliacoes/consulta/")
    print(f"CT06 - Status Consulta Avaliações: {response.status_code}")
    if response.status_code != 200:
        print(f"CT06 - Falha ao consultar avaliações: {response.text[:200]}")

    # CT09 - Acesso autenticado ao boletim do aluno
    # Página de boletim exibida com sucesso (status 200)
    @task(1)
    def acessar_boletim(self):
        response = self.client.get("/aluno/boletim/")
        print(f"CT09 - Status Acesso Boletim: {response.status_code}")
        if response.status_code != 200:
            print(f"CT09 - Falha no acesso ao boletim: {response.text[:200]}")
