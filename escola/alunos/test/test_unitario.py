from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from alunos.models import Aluno, Professor, Avaliacao, Presenca, Disciplina


# ===================== TESTES UNITÁRIOS COMPLETOS =====================

class TestSistemaEducacional(TestCase):
    """
    Testes do sistema educacional:
    - Cálculo de médias, aprovação e faltas
    - Registro de presença
    - Filtros de presenças
    - Exportação de PDF do dashboard do professor
    """

    def setUp(self):
        # Criação de usuários simulados
        self.user_aluno = User.objects.create(username="aluno", first_name="Ana", last_name="Beatriz")
        self.user_prof = User.objects.create(username="professor", first_name="Carlos", last_name="Silva")

        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula="12345")
        self.prof = Professor.objects.create(user=self.user_prof)
        self.disciplina = Disciplina.objects.create(nome="Matemática")

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
        from django.core.exceptions import ValidationError
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

    # CTU-18 – Nome completo do aluno
    def test_CTU008_nome_aluno(self):
        self.assertEqual(str(self.aluno), "Ana Beatriz")
        print("✅ CTU-18 OK - Nome completo do aluno exibido corretamente")

    # CTU-19 – Nome completo do professor
    def test_CTU009_nome_professor(self):
        self.assertEqual(str(self.prof), "Carlos Silva")
        print("✅ CTU-19 OK - Nome completo do professor exibido corretamente")

    # CTU-20 – Atualizar faltas e recalcular status
    def test_CTU010_atualizar_faltas_recalcula_status(self):
        avaliacao = Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8, nota_b2=8, faltas=2)
        avaliacao.faltas = 20
        avaliacao.save()
        self.assertEqual(avaliacao.status, "Reprovado por faltas")
        print("✅ CTU-20 OK - Atualização de faltas recalculou status corretamente")

    # ======== TESTES DE PRESENÇA ========

    # CTU-21 – Registrar presença do aluno
    def test_CTU011_registrar_presenca_aluno(self):
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            data=timezone.now().date(),
            presente=True
        )
        self.assertTrue(Presenca.objects.filter(aluno=self.aluno, presente=True).exists())
        print("✅ CTU-21 OK - Presença do aluno registrada corretamente")

    # ======== TESTE DE PDF ========

   # CTU-22 – Exportação do dashboard do professor em PDF
    def test_CTU013_exportar_dashboard_professor_pdf(self):
        Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=8, nota_b2=7, faltas=3)
        Avaliacao.objects.create(aluno=self.aluno, professor=self.prof, nota_b1=6, nota_b2=5, faltas=12)
        
        self.client.force_login(self.user_prof)
        url = reverse("exportar_pdf")
        response = self.client.get(url)
        
        # Verificações
        self.assertEqual(response.status_code, 200, "Falha ao exportar PDF")
        self.assertEqual(response["Content-Type"], "application/pdf", "Tipo de arquivo incorreto")
        self.assertIn(b"%PDF", response.content[:10], "Arquivo PDF inválido")
        
        print("✅ CTU-22 OK - Exportação do dashboard do professor para PDF funcionando corretamente")

    # ======== TESTE DE FILTRO ========

    # CTU-23– Filtro de presenças por disciplina
    def test_CTU014_filtrar_presencas_por_disciplina(self):
        outra_disciplina = Disciplina.objects.create(nome="História")
        Presenca.objects.create(aluno=self.aluno, disciplina=self.disciplina, data=timezone.now().date(), presente=True)
        Presenca.objects.create(aluno=self.aluno, disciplina=outra_disciplina, data=timezone.now().date(), presente=False)
        
        self.client.force_login(self.user_prof)
        
        response = self.client.get(reverse("presenca_professor"), {"disciplina": self.disciplina.nome})
        self.assertEqual(response.status_code, 200)

        # Deve conter a disciplina filtrada (Matemática)
        self.assertContains(response, self.disciplina.nome)

        # Verifica que não há registros da disciplina 'História' na tabela
        self.assertNotIn(b'<td>Hist\xc3\xb3ria</td>', response.content)
        print("✅ CTU- 23 OK- Filtro por disciplina funcionando corretamente")
