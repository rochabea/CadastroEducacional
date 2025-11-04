from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from alunos.models import Aluno, Professor, Avaliacao

# caso de teste 01: testa o cadastro de um aluno via formulário HTTP POST
class CadastroAlunoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastro_aluno')

    def test_cadastro_de_aluno_sucesso(self):
        # POST simulando o cadastro do aluno
        response = self.client.post(self.url, {
            'username': 'ana.bia',
            'password': 'senha123',
            'first_name': 'Ana',
            'last_name': 'Beatriz',
            'matricula': '20230120'
        })

        # Verifica redirecionamento (pós-cadastro) -> status 302
        self.assertEqual(response.status_code, 302)

        # Verifica se o usuário e o aluno foram criados no banco de dados
        user = User.objects.get(username='ana.bia')
        self.assertTrue(Aluno.objects.filter(user=user, matricula='20230120').exists())

# caso de teste 02: testa a criação direta de um professor no banco
class CadastroProfessorTest(TestCase):
    # cria o usuario e o professor manualmente
    def test_cadastro_professor_com_sucesso(self):
        user = User.objects.create_user(username='professor1', password='senha123', first_name='Carlos', last_name='Silva')
        professor = Professor.objects.create(user=user)
        
        # verifica se o userame está correto
        self.assertEqual(professor.user.username, 'professor1')
        # verifica se o método __str__ do professor retorna o nome completo
        self.assertEqual(str(professor), 'Carlos Silva')

# caso de teste 03: testa o cadastro de uma avaliação via POST
class CadastroAvaliacaoTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar usuário e professor para a avaliação
        self.user_prof = User.objects.create_user(username='maria', password='123')
        self.professor = Professor.objects.create(user=self.user_prof)

        # Criar usuário e aluno para avaliação
        self.user_aluno = User.objects.create_user(username='ana', password='123')
        self.aluno = Aluno.objects.create(user=self.user_aluno, matricula='20230121')

        self.url = reverse('lancar_avaliacao') # url que está na cadastrada para o lançamento

    def test_cadastro_avaliacao_media_status(self):
        self.client.force_login(self.user_prof)
        # enviar POST para cadastrar a avaliação
        response = self.client.post(self.url, {
            'aluno': self.aluno.id,
            'professor': self.professor.id,
            'nota_b1': 8.0,
            'nota_b2': 6.0,
            'faltas': 5
        })

        # verifica o redirecionamento após salvar avaliação
        self.assertEqual(response.status_code, 302)

        # busca avaliação criada e verifica se cálculo da médida e status estão corretos
        avaliacao = Avaliacao.objects.get(aluno=self.aluno)
        self.assertEqual(avaliacao.media, 7.0)
        self.assertEqual(avaliacao.status, 'Aprovado')

# caso de teste 04: testa reprovação por nota baixa
class ReprovacaoNotaTest(TestCase):
    def test_reprovacao_por_nota(self):
        # cria usuário, professor e aluno
        user_aluno = User.objects.create_user(username='aluno2', password='senha123')
        user_professor = User.objects.create_user(username='prof2', password='senha123')

        aluno = Aluno.objects.create(user=user_aluno, matricula='456')
        professor = Professor.objects.create(user=user_professor)

        # cria avaliações com notas baixas para reprovação
        avaliacao = Avaliacao.objects.create(
            aluno=aluno,
            professor=professor,
            nota_b1=5.0,
            nota_b2=4.0,
            faltas=5
        )

        # verifica se o status foi realmente de reprovação
        self.assertEqual(avaliacao.media, 4.5)
        self.assertEqual(avaliacao.status, 'Reprovado')

# caso de teste 05: testa reprovação por faltas excessivas
class ReprovacaoFaltasTest(TestCase):
    def test_reprovacao_por_faltas(self):
        user_aluno = User.objects.create_user(username='aluno3', password='senha123')
        user_professor = User.objects.create_user(username='prof3', password='senha123')

        aluno = Aluno.objects.create(user=user_aluno, matricula='789')
        professor = Professor.objects.create(user=user_professor)

        # cria avaliação com faltas acima do limite para reprovação
        avaliacao = Avaliacao.objects.create(
            aluno=aluno,
            professor=professor,
            nota_b1=9.0,
            nota_b2=8.0,
            faltas=20
        )

        # verifica se o resultado da média e o status o resultado é reprovação por faltas
        self.assertEqual(avaliacao.media, 8.5)
        self.assertEqual(avaliacao.status, 'Reprovado por faltas')

# caso de teste 06: testa a representação string do boletim do aluno (método __str__)
class BoletimAlunoTest(TestCase):
    def test_boletim_aluno(self):
        user = User.objects.create_user(username='aluno4', password='senha123', first_name='Maria', last_name='Oliveira')
        aluno = Aluno.objects.create(user=user, matricula='999')

        professor_user = User.objects.create_user(username='prof4', password='senha123')
        professor = Professor.objects.create(user=professor_user)

        # cria avaliação com notas e faltas
        avaliacao = Avaliacao.objects.create(
            aluno=aluno,
            professor=professor,
            nota_b1=7.0,
            nota_b2=9.0,
            faltas=3
        )

        # mostra a string esperada e compara com a saída __str__ do modelo Avaliacao
        boletim = f"{aluno} - Média: {avaliacao.media} - {avaliacao.status}"
        self.assertEqual(str(avaliacao), boletim)

# caso de teste 09: testa se o aluno consegue acessa a página do boletim aós login
class AcessoBoletimAlunoTest(TestCase):
    def setUp(self):
        self.client = Client()
        # cria usuário e aluno
        self.user = User.objects.create_user(username='aluno1', password='senha123', first_name='Alice')
        self.aluno = Aluno.objects.create(user=self.user, matricula='20230122')
        self.url = reverse('boletim_aluno')

    def test_acesso_boletim_apos_login(self):
        # realiza o login do aluno
        login_ok = self.client.login(username='aluno1', password='senha123')
        self.assertTrue(login_ok) # verifica se o login foi realizado com sucesso

        # faz requisição GET para página do boletim
        response = self.client.get(self.url)
        # verifica se a pa´gina carregou com sucesso -> status esperado é 200
        self.assertEqual(response.status_code, 200)
        # verifica se a palavra "boletim" aparece na resposta HTML
        self.assertContains(response, 'Boletim')  
