from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Aluno, Professor, Avaliacao

'''
class AvaliacaoConsultaTestCase(TestCase):
    def setUp(self):
        self.user_aluno = User.objects.create_user(username='aluno', password='123456')
        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula='20230356')

        self.user_prof = User.objects.create_user(username='prof', password='123456')
        self.professor = Professor.objects.create(user=self.user_prof, disciplina='Matemática')

        self.avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=7.5,
            nota_b2=8.0,
            media=7.75,
            status='Aprovado',
            faltas=2
        )

    def test_consulta_avaliacoes_por_aluno(self):
        self.client.login(username='ana.bia', password='Teste@1')
        response = self.client.get(reverse('boletim_aluno'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '7.5')
        self.assertContains(response, '8.0')
        self.assertContains(response, '7.75')
        self.assertContains(response, 'Aprovado')
'''


class CadastroAlunoTestCase(TestCase):
    def test_cadastro_aluno(self):
        response = self.client.post(reverse('cadastro_aluno'), {
            'username': 'bianca.andrade',
            'password': 'senha123',
            'first_name': 'Bianca',
            'last_name': 'Andrade',
            'matricula': '20230120'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertTrue(Aluno.objects.filter(matricula='20230120').exists())


class CadastroProfessorTestCase(TestCase):
    def test_cadastro_professor(self):
        response = self.client.post(reverse('cadastro_professor'), {
            'username': 'thais.santos',
            'password': 'senha123',
            'first_name': 'Thais',
            'last_name': 'Santos'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Professor.objects.filter(user__username='thais.santos').exists())  # Corrigido username


class AvaliacaoOperacoesTestCase(TestCase):
    def setUp(self):
        # Criação dos usuários
        self.user_aluno = User.objects.create_user(
            username='alice.beatriz', password='senha123',
            first_name='Alice', last_name='Beatriz'
        )
        self.user_professor = User.objects.create_user(
            username='thais.santos', password='senha123',
            first_name='Thais', last_name='Santos'
        )

        # Criação dos perfis
        self.aluno = Aluno.objects.create(
            user=self.user_aluno,
            matricula='20230356'
        )
        self.professor = Professor.objects.create(
            user=self.user_professor
        )

    def test_cadastro_avaliacao(self):
        self.client.login(username='thais.santos', password='senha123')
        response = self.client.post(reverse('lancar_avaliacao'), {
            'aluno': self.aluno.id,
            'nota_b1': 7.5,
            'nota_b2': 8.0,
            'faltas': 5
        })
        self.assertEqual(response.status_code, 302)
        avaliacao = Avaliacao.objects.get(aluno=self.aluno)
        self.assertEqual(avaliacao.media, 7.75) 
        self.assertEqual(avaliacao.status, 'Aprovado')

    def test_calculo_media(self):
        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=5.0,
            nota_b2=7.0,
            faltas=2
        )
        self.assertEqual(avaliacao.media, 6.0)  

    def test_calculo_status_reprovado_por_faltas(self):
        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=6.0,
            nota_b2=6.0,
            faltas=11
        )
        self.assertEqual(avaliacao.status, 'Reprovado')

    def test_consulta_avaliacoes_por_aluno(self):
        self.client.login(username='alice.beatriz', password='senha123')
        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=7.5,
            nota_b2=8.0,
            faltas=2
        )
        response = self.client.get(reverse('boletim_aluno'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '7.5')
        self.assertContains(response, '8.0')
        self.assertContains(response, '7.75')
        self.assertContains(response, 'Aprovado')




    def test_validacao_matricula_unica(self):
        User.objects.create_user(
            username='eduarda.macedo', password='senha123'
        )
        Aluno.objects.create(
            user=User.objects.get(username='eduarda.macedo'),
            matricula='20145698'
        )
        response = self.client.post(reverse('cadastro_aluno'), {
            'username': 'arthur.padro',
            'password': 'senha123',
            'first_name': 'Arthur',
            'last_name': 'Padro',
            'matricula': '20145698'  # Matrícula duplicada proposital
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Matrícula já cadastrada')


    def test_validacao_notas_invalidas(self):
        self.client.login(username='thais.santos', password='senha123')
        response = self.client.post(reverse('lancar_avaliacao'), {
            'aluno': self.aluno.id,
            'nota_b1': -1.0,  # Nota inválida
            'nota_b2': 11.0,  # Nota inválida
            'faltas': 0
        })
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode(), r'nota.*entre 0 e 10')
        


