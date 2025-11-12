from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import resolve_url
from alunos.models import Aluno, Professor, Avaliacao, Presenca, Disciplina
from django.core.exceptions import ValidationError


# ===================== TESTES UNITÁRIOS COMPLETOS =====================

class TestSistemaEducacional(TestCase):
    """
    Testes do sistema educacional:
    - Cálculo de médias, aprovação e faltas
    - Registro e filtro de presenças
    - Exportação de PDF do dashboard do professor
    - Feedbacks
    - Logout de usuários
    """

    def setUp(self):
        """Cria dados simulados para todos os testes."""
        self.user_aluno = User.objects.create(username="aluno", first_name="Ana", last_name="Beatriz")
        self.user_prof = User.objects.create(username="professor", first_name="Carlos", last_name="Silva")

        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula="12345")
        self.prof = Professor.objects.create(user=self.user_prof)
        self.disciplina = Disciplina.objects.create(nome="Matemática")

    # ===================== AVALIAÇÃO =====================

    # CTU-01 – Média correta
    def test_CTU001_media_calculada(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8.0, nota_b2=6.0, faltas=5)
        self.assertEqual(avaliacao.media, 7.00)
        print("✅ CTU-01 OK - Média calculada corretamente")

    # CTU-02 – Status aprovado
    def test_CTU002_status_aprovado(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=9.0, nota_b2=8.0, faltas=5)
        self.assertEqual(avaliacao.status, "Aprovado")
        print("✅ CTU-02 OK - Status aprovado validado corretamente")

    # CTU-03 – Reprovado por faltas
    def test_CTU003_reprovado_faltas(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=9.0, nota_b2=8.0, faltas=20)
        self.assertEqual(avaliacao.status, "Reprovado por faltas")
        print("✅ CTU-03 OK - Reprovação por faltas validada corretamente")

    # CTU-04 – Reprovado por média baixa
    def test_CTU004_reprovado_media_baixa(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=4.0, nota_b2=5.0, faltas=2)
        self.assertEqual(avaliacao.status, "Reprovado")
        print("✅ CTU-04 OK - Reprovação por média baixa validada corretamente")

    # CTU-15 – Notas fora do intervalo
    def test_CTU005_notas_invalidas(self):
        avaliacao = Avaliacao(aluno=self.aluno, professor=self.prof, nota_b1=12, nota_b2=8, faltas=2)
        with self.assertRaises(ValidationError):
            avaliacao.clean()
        print("✅ CTU-15 OK - Validação de notas inválidas funcionando")

    # CTU-16 – Média arredondada corretamente
    def test_CTU006_media_arredondada(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=7.35, nota_b2=6.75, faltas=0)
        self.assertEqual(avaliacao.media, 7.05)
        print("✅ CTU-16 OK - Arredondamento da média validado")

    # CTU-17 – String de avaliação formatada
    def test_CTU007_str_avaliacao(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=7, nota_b2=7, faltas=0)
        self.assertIn("Média", str(avaliacao))
        print("✅ CTU-17 OK - String de avaliação exibida corretamente")

    # CTU-18 – Logout do usuário
    def test_CTU008_logout_usuario(self):
        """Verifica se o logout é executado corretamente."""
        self.client.force_login(self.user_aluno)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        print("✅ CTU-18 OK - Logout do usuário realizado com sucesso")

    # CTU-19 – Feedback do professor e aluno
    def test_CTU009_feedback_professor_aluno(self):
        """Testa o envio e exibição de feedbacks entre professor e aluno."""

        self.client.force_login(self.user_prof)
        url_novo = resolve_url("/professor/feedbacks/novo/")
        url_list = resolve_url("/professor/feedbacks/")

        # Acessa página de novo feedback
        response_get = self.client.get(url_novo)
        self.assertEqual(response_get.status_code, 200)

        response_post = self.client.post(url_novo, {
            "aluno": self.aluno.id,
            "texto": "Excelente desempenho nas atividades!",
            "visivel_para_aluno": True
        })
        self.assertEqual(response_post.status_code, 302)

        # Verifica listagem
        response_list = self.client.get(url_list)
        self.assertEqual(response_list.status_code, 200)
        self.assertContains(response_list, "Excelente desempenho")

        print("✅ CTU-19 OK - Feedback do professor e aluno funcionando corretamente")

    # CTU-20 – Atualizar faltas e recalcular status
    def test_CTU010_atualizar_faltas_recalcula_status(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8, nota_b2=8, faltas=2)
        avaliacao.faltas = 20
        avaliacao.save()
        self.assertEqual(avaliacao.status, "Reprovado por faltas")
        print("✅ CTU-20 OK - Atualização de faltas recalculou status corretamente")

    # ===================== PRESENÇA =====================

    # CTU-21 – Registrar presença do aluno
    def test_CTU011_registrar_presenca_aluno(self):
        Presenca.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=timezone.now().date(),
            presente=True
        )
        self.assertTrue(Presenca.objects.filter(aluno=self.aluno, presente=True).exists())
        print("✅ CTU-21 OK - Presença do aluno registrada corretamente")

    # CTU-22 – Filtro de presenças por disciplina
    def test_CTU012_filtrar_presencas_por_disciplina(self):
        outra_disciplina = Disciplina.objects.create(nome="História")
        Presenca.objects.create(aluno=self.aluno, disciplina=self.disciplina, data=timezone.now().date(), presente=True)
        Presenca.objects.create(aluno=self.aluno, disciplina=outra_disciplina, data=timezone.now().date(), presente=False)
        
        self.client.force_login(self.user_prof)
        response = self.client.get(reverse("presenca_professor"), {"disciplina": self.disciplina.nome})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.disciplina.nome)
        self.assertNotIn(b'<td>Hist\xc3\xb3ria</td>', response.content)
        print("✅ CTU-22 OK - Filtro por disciplina funcionando corretamente")

    # ===================== PDF EXPORT =====================

    # CTU-23 – Exportação do dashboard do professor em PDF
    def test_CTU013_exportar_dashboard_professor_pdf(self):
        Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8, nota_b2=7, faltas=3)
        Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=6, nota_b2=5, faltas=12)
        
        self.client.force_login(self.user_prof)
        url = reverse("exportar_pdf")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200, "Falha ao exportar PDF")
        self.assertEqual(response["Content-Type"], "application/pdf", "Tipo de arquivo incorreto")
        self.assertIn(b"%PDF", response.content[:10], "Arquivo PDF inválido")

        print("✅ CTU-23 OK - Exportação do dashboard do professor para PDF funcionando corretamente")
