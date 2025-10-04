from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from alunos.models import Aluno, Professor, Feedback

class FeedbackViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_aluno_ve_apenas_seus_feedbacks(self):
        u1 = User.objects.create_user('aluno1', password='senhaAluno123')
        u2 = User.objects.create_user('aluno2', password='senhaAluno123')
        a1 = Aluno.objects.create(user=u1, matricula='M1')
        a2 = Aluno.objects.create(user=u2, matricula='M2')
        up = User.objects.create_user('prof1', password='senhaProf123')
        p  = Professor.objects.create(user=up)
        Feedback.objects.create(aluno=a1, professor=p, texto='F01', visivel_para_aluno=True)
        Feedback.objects.create(aluno=a2, professor=p, texto='F02', visivel_para_aluno=True)

        self.client.login(username='aluno1', password='senhaAluno123')
        resp = self.client.get(reverse('aluno-meus-feedbacks'))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn('F01', html)
        self.assertNotIn('F02', html)

    def test_professor_cria_e_lista_feedbacks(self):
        up = User.objects.create_user('prof1', password='senhaProf123')
        p  = Professor.objects.create(user=up)
        ua = User.objects.create_user('aluno1', password='senhaAluno123')
        a  = Aluno.objects.create(user=ua, matricula='M1')

        self.client.login(username='prof1', password='senhaProf123')

        # cria via view de criação
        resp = self.client.post(
            reverse('feedback-create'),
            data={'aluno': a.id, 'texto': 'Novo FB', 'visivel_para_aluno': True}
        )
        self.assertIn(resp.status_code, (301, 302))

        # lista do professor
        resp = self.client.get(reverse('prof-meus-feedbacks'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Novo FB', resp.content.decode())
