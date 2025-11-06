from django.test import TestCase
from django.contrib.auth.models import User
from alunos.models import Aluno, Professor, Avaliacao

# ===================== TESTES UNITÁRIOS - REGRAS DE AVALIAÇÃO =====================

class TestAvaliacao(TestCase):

    def setUp(self):
        # Usuário base para simular aluno e professor
        self.user_aluno = User.objects.create(username="aluno", first_name="Ana", last_name="Beatriz")
        self.user_prof = User.objects.create(username="professor", first_name="Carlos", last_name="Silva")

        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula="12345")
        self.prof = Professor.objects.create(user=self.user_prof)

    # CASO DE TESTE CTU-01 – Média correta
    def test_CTU001_media_calculada(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8.0, nota_b2=6.0, faltas=5)
        self.assertEqual(avaliacao.media, 7.00, "CTU-001 FALHOU X - A média deveria ser 7.00")
        print("✅ CTU-01 OK - Média calculada corretamente")

    # CASO DE TESTE CTU-02 – Status aprovado
    def test_CTU002_status_aprovado(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=9.0, nota_b2=8.0, faltas=5)
        self.assertEqual(avaliacao.status, "Aprovado", "CTU-002 FALHOU X - O status deveria ser Aprovado")
        print("✅ CTU-02 OK - Status aprovado validado corretamente")

    # CASO DE TESTE CTU-03 – Reprovado por faltas
    def test_CTU003_reprovado_faltas(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=9.0, nota_b2=8.0, faltas=20)
        self.assertEqual(avaliacao.status, "Reprovado por faltas", "CTU-003 FALHOU X - O status deveria ser Reprovado por faltas")
        print("✅ CTU-03 OK - Reprovação por faltas validada corretamente")

    # CASO DE TESTE CTU-04 – Reprovado por média baixa
    def test_CTU004_reprovado_media_baixa(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=4.0, nota_b2=5.0, faltas=2)
        self.assertEqual(avaliacao.status, "Reprovado", "CTU-004 FALHOU X - O status deveria ser Reprovado")
        print("✅ CTU-04 OK - Reprovação por média baixa validada corretamente")
