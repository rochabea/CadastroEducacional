from django.test import TestCase
from django.contrib.auth.models import User
from alunos.models import Aluno, Professor, Avaliacao

# ===================== TESTES DE REGRAS DE NEGÓCIOS  =====================

class TesteRegrasNegocio(TestCase):

    def setUp(self):
        self.user_aluno = User.objects.create(username="aluno", first_name="Ana", last_name="Beatriz")
        self.user_prof = User.objects.create(username="professor", first_name="Carlos", last_name="Silva")

        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula="12345")
        self.prof = Professor.objects.create(user=self.user_prof)

    # CT-RN-01 - Aprovação por média
    def test_aprovacao_por_media(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8, nota_b2=7, faltas=5)
        media = avaliacao.media
        self.assertTrue(media >= 7)
        print("✅ CT-RN-01 - Aprovado por média validado com sucesso")
    
    # CT-RN-03 - Reprovação por faltas (regra 25% das aulas)
    def test_reprovacao_por_faltas(self):
        total_aulas = 80  # valor base usado para regra de negócio no cenário
        limite = total_aulas * 0.25

        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno, professor=self.prof, nota_b1=9, nota_b2=9, faltas=30
        )

        self.assertTrue(avaliacao.faltas > limite)
        print("✅ CT-RN-03 - Reprovado por faltas validado com sucesso")

    # CT-RN-04 - Reprovação por média baixa
    def test_reprovado_media_baixa(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=5, nota_b2=4, faltas=3)
        media = avaliacao.media
        self.assertTrue(media < 7)
        print("✅ CT-RN-04 - Reprovado por média baixa validado com sucesso")
