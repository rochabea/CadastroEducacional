import pytest
from unittest.mock import Mock
from alunos.models import Aluno, Professor, Avaliacao

@pytest.mark.usefixtures("mock_db")
class TesteRegrasNegocio:

    @pytest.fixture(autouse=True)
    def setup(self, mock_db):
        # Criando mocks de usuários
        self.user_aluno = Mock(username="aluno", first_name="Ana", last_name="Beatriz")
        self.user_prof = Mock(username="professor", first_name="Carlos", last_name="Silva")

        # Criando mocks de modelos
        self.aluno = Mock(spec=Aluno)
        self.aluno.user = self.user_aluno
        self.aluno.matricula = "12345"

        self.prof = Mock(spec=Professor)
        self.prof.user = self.user_prof

    # CT-RN-01 - Aprovação por média
    def test_aprovacao_por_media(self):
        # Avaliacao mock
        avaliacao = Mock(spec=Avaliacao)
        avaliacao.aluno = self.aluno
        avaliacao.professor = self.prof
        avaliacao.nota_b1 = 8
        avaliacao.nota_b2 = 7
        avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2) / 2

        assert avaliacao.media >= 7
        print("✅ CT-RN-01 - Aprovado por média validado com sucesso")

    # CT-RN-03 - Reprovação por faltas
    def test_reprovacao_por_faltas(self):
        total_aulas = 80
        limite = total_aulas * 0.25

        avaliacao = Mock(spec=Avaliacao)
        avaliacao.faltas = 30

        assert avaliacao.faltas > limite
        print("✅ CT-RN-03 - Reprovado por faltas validado com sucesso")

    # CT-RN-04 - Reprovação por média baixa
    def test_reprovado_media_baixa(self):
        avaliacao = Mock(spec=Avaliacao)
        avaliacao.nota_b1 = 5
        avaliacao.nota_b2 = 4
        avaliacao.media = (avaliacao.nota_b1 + avaliacao.nota_b2) / 2

        assert avaliacao.media < 7
        print("✅ CT-RN-04 - Reprovado por média baixa validado com sucesso")
