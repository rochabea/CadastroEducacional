from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from alunos.models import Aluno, Professor, Avaliacao

class TestFuncionais(TestCase):

    def test_ct01_cadastro_de_aluno(self):
        dados = {
            'username': 'ana.bia',
            'first_name': 'Ana',
            'last_name': 'Bia',
            'email': 'ana@email.com',
            'password': 'teste123',
            'matricula': '20230120'
        }
        response = self.client.post(reverse('cadastro_aluno'), data=dados)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.get(username='ana.bia')
        aluno = Aluno.objects.get(user=user)
        self.assertEqual(aluno.matricula, '20230120')

    def test_ct02_login_como_aluno(self):
        user = User.objects.create_user(username='joao', password='senha123')
        Aluno.objects.create(user=user, matricula='A123')
        
        login_data = {'username': 'joao', 'password': 'senha123'}
        response = self.client.post(reverse('login'), data=login_data)
        self.assertRedirects(response, reverse('dashboard_aluno'))

    def test_ct03_cadastro_professor(self):
        dados = {
            'username': 'prof123',
            'first_name': 'Carlos',
            'last_name': 'Silva',
            'email': 'carlos@email.com',
            'password': 'profpass123'
        }
        prof_form = {
            'username': dados['username'],
            'first_name': dados['first_name'],
            'last_name': dados['last_name'],
            'email': dados['email'],
            'password': dados['password']
        }
        response = self.client.post(reverse('cadastro_professor'), data=prof_form)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.get(username='prof123')
        self.assertTrue(Professor.objects.filter(user=user).exists())

    def test_ct04_lancar_avaliacao(self):
        # Cria professor e login
        user = User.objects.create_user(username='prof', password='prof123')
        prof = Professor.objects.create(user=user)
        self.client.login(username='prof', password='prof123')

        # Cria aluno
        aluno_user = User.objects.create_user(username='aluno', password='aluno123')
        aluno = Aluno.objects.create(user=aluno_user, matricula='999')

        # Dados da avaliação
        dados = {
            'aluno': aluno.id,
            'nota_b1': 8.0,
            'nota_b2': 7.5,
            'faltas': 3
        }

        response = self.client.post(reverse('lancar_avaliacao'), data=dados)
        self.assertRedirects(response, reverse('dashboard_professor'))

        avaliacao = Avaliacao.objects.get(aluno=aluno)
        self.assertEqual(avaliacao.media, 7.75)
        self.assertEqual(avaliacao.status, 'Aprovado')

    def test_ct05_boletim_aluno(self):
        # Cria aluno e professor
        user = User.objects.create_user(username='ana', password='ana123')
        aluno = Aluno.objects.create(user=user, matricula='777')
        prof_user = User.objects.create_user(username='prof1', password='p1')
        prof = Professor.objects.create(user=prof_user)

        # Cria avaliação com save() para garantir que status seja calculado
        avaliacao = Avaliacao(aluno=aluno, professor=prof, nota_b1=5, nota_b2=6, faltas=2)
        avaliacao.save()

        self.client.force_login(user)
        response = self.client.get(reverse('boletim_aluno'))

        # Verifica se notas estão na resposta
        self.assertContains(response, '5')
        self.assertContains(response, '6')

        # Verifica se média está na resposta, formatada como string, com 2 casas decimais
        media_str = f"{avaliacao.media:.2f}"  # '5.50'
        self.assertContains(response, media_str)

        # Verifica status
        self.assertContains(response, avaliacao.status)  # deve ser 'Reprovado'


    

