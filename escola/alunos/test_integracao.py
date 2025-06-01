from django.test import TestCase
from django.contrib.auth.models import User
from .models import Aluno, Professor, Avaliacao


class TestIntegracaoCadastro(TestCase):

    def test_cadastro_aluno_professor_avaliacao(self):
        # Criar usuários
        user_aluno = User.objects.create_user(
            username='ana.bia', first_name='Ana', last_name='Bia'
        )
        user_prof = User.objects.create_user(
            username='maria.oliveira', first_name='Maria', last_name='Oliveira'
        )

        # Criar Aluno
        aluno = Aluno.objects.create(user=user_aluno, matricula='20230120')

        # Criar Professor
        professor = Professor.objects.create(user=user_prof)

        # Criar Avaliação
        avaliacao = Avaliacao.objects.create(
            aluno=aluno,
            professor=professor,
            nota_b1=7.5,
            nota_b2=8.0,
            faltas=5
        )

        # Verificações
        self.assertEqual(avaliacao.media, 7.75)
        self.assertEqual(avaliacao.status, 'Aprovado')
        self.assertEqual(avaliacao.aluno.user.get_full_name(), 'Ana Bia')
        self.assertEqual(avaliacao.professor.user.get_full_name(), 'Maria Oliveira')
