from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Aluno, Professor, Avaliacao


class CadastroAlunoIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastro_aluno')

    def test_ct01_cadastro_de_aluno(self):
        user_data = {
            'username': 'ana.bia',
            'password': 'senha123',
            'first_name': 'Ana',
            'last_name': 'Bia',
            'email': 'ana.bia@email.com',
        }
        aluno_data = {
            'matricula': '20230120'
        }
        post_data = {**user_data, **aluno_data}

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(username='ana.bia').exists())
        user = User.objects.get(username='ana.bia')
        self.assertEqual(user.first_name, 'Ana')
        self.assertEqual(user.last_name, 'Bia')

        self.assertTrue(Aluno.objects.filter(user=user, matricula='20230120').exists())


class CadastroProfessorIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastro_professor')

    def test_ct02_cadastro_de_professor(self):
        user_data = {
            'username': 'maria.oliveira',
            'password': 'senha123',
            'first_name': 'Maria',
            'last_name': 'Oliveira',
            'email': 'maria.oliveira@email.com',
        }
        professor_data = {}
        post_data = {**user_data, **professor_data}

        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(username='maria.oliveira').exists())
        user = User.objects.get(username='maria.oliveira')

        self.assertTrue(Professor.objects.filter(user=user).exists())


class CadastroAvaliacaoIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('lancar_avaliacao')

        self.user_aluno = User.objects.create_user(username='ana.bia', password='senha123')
        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula='20230120')

        self.user_professor = User.objects.create_user(username='maria.oliveira', password='senha123')
        self.professor = Professor.objects.create(user=self.user_professor)

    def test_ct03_cadastro_de_avaliacao(self):
        # precisa do acesso do professor para lançar a nota
        self.client.login(username='maria.oliveira', password='senha123')
        
        post_data = {
            'aluno': self.aluno.id,
            'professor': self.professor.id,
            'nota_b1': 7.5,
            'nota_b2': 8.0,
            'faltas': 5,
        }
        response = self.client.post(self.url, post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard_professor'))

        avaliacao = Avaliacao.objects.get(aluno=self.aluno, professor=self.professor)
        media_esperada = (7.5 + 8.0) / 2
        self.assertAlmostEqual(avaliacao.media, media_esperada)
        self.assertEqual(avaliacao.status, 'Aprovado')


class ConsultaAvaliacoesAlunoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_aluno = User.objects.create_user(username='ana.bia', password='senha123')
        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula='20230120')
        self.url = reverse('consulta_avaliacoes')

        self.professor = Professor.objects.create(user=User.objects.create_user(username='prof1', password='senha123'))
        Avaliacao.objects.create(aluno=self.aluno, professor=self.professor, nota_b1=7, nota_b2=8, faltas=2)
        outro_aluno = Aluno.objects.create(user=User.objects.create_user(username='outro', password='senha123'), matricula='20230001')
        Avaliacao.objects.create(aluno=outro_aluno, professor=self.professor, nota_b1=6, nota_b2=5, faltas=0)

    def test_ct06_consulta_avaliacoes(self):
        self.client.login(username='ana.bia', password='senha123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        avaliacoes = response.context['avaliacoes']
        for avaliacao in avaliacoes:
            self.assertEqual(avaliacao.aluno, self.aluno)


class AcessoBoletimAlunoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_aluno = User.objects.create_user(username='alice.beatriz', password='senha123')
        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula='20230002')
        self.url_boletim = reverse('boletim_aluno')

    def test_ct09_acesso_boletim(self):
        login = self.client.login(username='alice.beatriz', password='senha123')
        self.assertTrue(login)

        response = self.client.get(self.url_boletim)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Boletim')
