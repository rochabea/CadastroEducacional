from locust import HttpUser, task, between
import re

# ===================== TESTE DE STRESS - DESEMPENHO =====================

class UsuarioAluno(HttpUser):
    wait_time = between(0.5, 1)  # tempo de espera entre ações

    def on_start(self):
        """Login antes de iniciar as tarefas"""
        response = self.client.get("/login/")
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', response.text)
        csrf_token = match.group(1) if match else None
   
    # CASO DE TESTE CTU-05 E CTU-06
        if csrf_token:
            login_response = self.client.post(
                "/login/",
                data={
                    "username": "alice.beatriz",
                    "password": "senha123",
                    "csrfmiddlewaretoken": csrf_token
                },
                headers={"Referer": "http://127.0.0.1:8000/login/"},
                allow_redirects=True
            )
            if login_response.status_code in [200, 302]:
                print("CT05 - CT06 - Login realizado com sucesso.")
            else:
                print(f"Falha no login: {login_response.status_code}")
        else:
            print("CSRF token não encontrado. Login não realizado.")

    @task(3)
    # CASO DE TESTE CTU-07

    def acessar_dashboard_aluno(self):
        response = self.client.get("/dashboard/aluno/")
        if response.status_code == 200:
            print("CT07-Dashboard do aluno acessado com sucesso.")
        else:
            print(f"Falha ao acessar dashboard: {response.status_code}")

    @task(2)
    # CASO DE TESTE CTU-08

    def acessar_quadro_horario(self):
        response = self.client.get("/dashboard/quadro_horario_aluno/")
        if response.status_code == 200:
            print("CT08 -Quadro de horário acessado com sucesso.")
        else:
            print(f"Falha ao acessar quadro de horário: {response.status_code}")

    @task(2)
    # CASO DE TESTE CTU-09

    def acessar_feedbacks(self):
        response = self.client.get("/aluno/feedbacks/")
        if response.status_code == 200:
            print("CT09 -Feedbacks acessados com sucesso.")
        else:
            print(f"Falha ao acessar feedbacks: {response.status_code}")

    @task(1)
    # CASO DE TESTE CTU-10

    def acessar_presenca_alunos(self):
        response = self.client.get("/dashboard/presenca_alunos/")
        if response.status_code == 200:
            print("CT10 -Presença do aluno acessada com sucesso.")
        else:
            print(f"Falha ao acessar presença: {response.status_code}")
