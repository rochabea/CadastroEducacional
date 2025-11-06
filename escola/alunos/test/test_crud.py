from django.test import TestCase
from django.contrib.auth.models import User
from alunos.models import Aluno, Professor, Avaliacao
from alunos.forms import AvaliacaoForm

# ===================== TESTE DE CRUD - LANÇAR AVALIAÇÃO  =====================

class AvaliacaoFormTestCase(TestCase):

    def setUp(self):
        # Criar usuário e aluno
        self.user_aluno = User.objects.create_user(username='aluno', password='12345')
        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula='12345678')

        # Criar usuário e professor
        self.user_professor = User.objects.create_user(username='professor', password='12345')
        self.professor = Professor.objects.create(user=self.user_professor)

    # ===================== CREATE =====================
    def test_create_avaliacao_valida(self):
        form_data = {
            'aluno': self.aluno.id,
            'nota_b1': 8.0,
            'nota_b2': 7.5,
            'faltas': 2
        }
        # Cria o form
        form = AvaliacaoForm(data=form_data)
        # Antes de validar, associamos o professor, porque é obrigatório no modelo
        avaliacao = form.save(commit=False)
        avaliacao.professor = self.professor
        try:
            avaliacao.full_clean()  
        except Exception as e:
            self.fail(f"Falha na validação do modelo: {e}")
        avaliacao.save() # Salva no banco

        # Verificações
        self.assertEqual(avaliacao.aluno, self.aluno)
        self.assertEqual(avaliacao.professor, self.professor)
        self.assertEqual(avaliacao.nota_b1, 8.0)
        self.assertEqual(avaliacao.nota_b2, 7.5)
        self.assertEqual(avaliacao.faltas, 2)
        self.assertEqual(avaliacao.status, 'Aprovado')



    # ===================== READ =====================
    def test_read_avaliacao(self):
        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=6.0,
            nota_b2=7.0,
            faltas=1
        )
        found = Avaliacao.objects.get(id=avaliacao.id)
        self.assertEqual(found.nota_b1, 6.0)
        self.assertEqual(found.nota_b2, 7.0)
        self.assertEqual(found.faltas, 1)

    # ===================== UPDATE =====================
    def test_update_avaliacao(self):
        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=5.0,
            nota_b2=5.0,
            faltas=3
        )
        form_data = {
            'aluno': self.aluno.id,
            'nota_b1': 7.0,
            'nota_b2': 8.0,
            'faltas': 2
        }
        form = AvaliacaoForm(data=form_data, instance=avaliacao)
        self.assertTrue(form.is_valid())
        updated = form.save(commit=False)
        updated.professor = self.professor
        updated.save()

        self.assertEqual(updated.nota_b1, 7.0)
        self.assertEqual(updated.nota_b2, 8.0)
        self.assertEqual(updated.faltas, 2)

    # ===================== DELETE =====================
    def test_delete_avaliacao(self):
        avaliacao = Avaliacao.objects.create(
            aluno=self.aluno,
            professor=self.professor,
            nota_b1=9.0,
            nota_b2=9.5,
            faltas=0
        )
        avaliacao_id = avaliacao.id
        avaliacao.delete()
        with self.assertRaises(Avaliacao.DoesNotExist):
            Avaliacao.objects.get(id=avaliacao_id)
