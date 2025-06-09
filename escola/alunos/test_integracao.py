from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .models import Aluno, Professor, Avaliacao


class TestIntegracao(TestCase):

    def setUp(self):
    # Professor padrão para reutilizar nos testes
        self.user_prof = User.objects.create_user(username='prof1', first_name='Prof', last_name='Padrão')
        self.professor = Professor.objects.create(user=self.user_prof)

    # CT01 - Cadastro de Aluno
    def test_ct01_cadastro_aluno(self):
        user = User.objects.create_user(username='aluno1', first_name='Ana', last_name='Bia')
        aluno = Aluno.objects.create(user=user, matricula='20230001')
        self.assertEqual(aluno.matricula, '20230001')
        self.assertEqual(aluno.user.get_full_name(), 'Ana Bia')

    # CT02 - Cadastro de Professor
    def test_ct02_cadastro_professor(self):
        user = User.objects.create_user(username='prof2', first_name='Maria', last_name='Oliveira')
        professor = Professor.objects.create(user=user)
        self.assertEqual(str(professor), 'Maria Oliveira')

    # CT03 - Cadastro de Avaliação
    def test_ct03_cadastro_avaliacao(self):
        user = User.objects.create_user(username='aluno2')
        aluno = Aluno.objects.create(user=user, matricula='20230002')
        avaliacao = Avaliacao.objects.create(aluno=aluno, professor=self.professor, nota_b1=6.0, nota_b2=8.0, faltas=4)
        self.assertEqual(avaliacao.media, 7.0)
        self.assertIn(avaliacao.status, ['Aprovado', 'Reprovado', 'Reprovado por faltas'])

    # CT04 - Cálculo Automático de Média
    def test_ct04_calculo_automatico_media(self):
        user = User.objects.create_user(username='aluno3')
        aluno = Aluno.objects.create(user=user, matricula='20230003')
        avaliacao = Avaliacao.objects.create(aluno=aluno, professor=self.professor, nota_b1=9.0, nota_b2=7.0, faltas=1)
        self.assertEqual(avaliacao.media, 8.0)

    # CT05 - Cálculo Automático de Status
    def test_ct05_calculo_automatico_status(self):
        user = User.objects.create_user(username='aluno4')
        aluno = Aluno.objects.create(user=user, matricula='20230004')
        avaliacao = Avaliacao.objects.create(aluno=aluno, professor=self.professor, nota_b1=5.0, nota_b2=5.0, faltas=2)
        self.assertEqual(avaliacao.status, 'Reprovado')

    # CT06 - Consulta de Avaliações por Aluno
    def test_ct06_consulta_avaliacoes_por_aluno(self):
        user = User.objects.create_user(username='aluno5')
        aluno = Aluno.objects.create(user=user, matricula='20230005')
        Avaliacao.objects.create(aluno=aluno, professor=self.professor, nota_b1=7.0, nota_b2=8.0, faltas=2)
        Avaliacao.objects.create(aluno=aluno, professor=self.professor, nota_b1=9.0, nota_b2=10.0, faltas=0)
        avaliacoes = Avaliacao.objects.filter(aluno=aluno)
        self.assertEqual(avaliacoes.count(), 2)

    # CT07 - Validação de Matrícula Única
    def test_ct07_validacao_matricula_unica(self):
        user1 = User.objects.create_user(username='aluno6')
        user2 = User.objects.create_user(username='aluno7')
        Aluno.objects.create(user=user1, matricula='20230006')
        with self.assertRaises(IntegrityError):
            # matrícula duplicada
            Aluno.objects.create(user=user2, matricula='20230006')  

    # CT08 - Validação de Notas Inválidas
    def test_ct08_validacao_notas_invalidas(self):
        user = User.objects.create_user(username='aluno8')
        aluno = Aluno.objects.create(user=user, matricula='20230008')
        with self.assertRaises(ValidationError):
            avaliacao = Avaliacao(
                aluno=aluno,
                professor=self.professor,
                # nota inválida (>10)
                nota_b1=11,  
                nota_b2=8,
                faltas=0
            )
            # dispara validação de notas
            avaliacao.full_clean()  
