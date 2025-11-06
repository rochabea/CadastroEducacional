from locust import HttpUser, task, between
import re

# ===================== TESTE DE CARGA - DESEMPENHO  =====================

class UsuarioAluno(HttpUser):
    wait_time = between(1, 3)  

    def on_start(self):
        response = self.client.get("/login/")
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', response.text)
        if match:
            self.csrf_token = match.group(1)
        else:
            print("CSRF token não encontrado!")
            return

    # CASO DE TESTE CTU-05 E CTU-06
        login_response = self.client.post(
            "/login/",
            data={
                "username": "alice.beatriz",  # usuário de teste
                "password": "senha123",
                "csrfmiddlewaretoken": self.csrf_token
            },
            headers={"Referer": "http://127.0.0.1:8000/login/"},
            allow_redirects=True
        )
        if login_response.status_code in [200, 302]:
            print("Login realizado com sucesso!")
        else:
            print(f"Falha no login: {login_response.status_code}")

    # ===================== Páginas do aluno =====================
    # CASO DE TESTE CTU-07
    @task(3)
    def acessar_dashboard_aluno(self):
        response = self.client.get("/dashboard/aluno/")
        print(f"Status /dashboard/aluno/: {response.status_code}")
    # CASO DE TESTE CTU-08
    @task(2)
    def acessar_quadro_horario(self):
        response = self.client.get("/dashboard/quadro_horario_aluno/")
        print(f"Status /dashboard/quadro_horario_aluno/: {response.status_code}")
    # CASO DE TESTE CTU-09
    @task(2)
    def acessar_feedbacks(self):
        response = self.client.get("/aluno/feedbacks/")
        print(f"Status /aluno/feedbacks/: {response.status_code}")
    # CASO DE TESTE CTU-10
    @task(1)
    def acessar_presenca_alunos(self):
        response = self.client.get("/dashboard/presenca_alunos/")
        print(f"Status /dashboard/presenca_alunos/: {response.status_code}")
