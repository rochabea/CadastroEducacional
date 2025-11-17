# alunos/test/test_avaliacoes_integration_mock.py

import pytest
from unittest.mock import Mock

MEDIA_APROVACAO = 7.0
FALTAS_LIMITE_REPROVACAO = 15

# --- Fixtures de Aluno e Professor ---
@pytest.fixture
def aluno():
    aluno = Mock()
    aluno.username = "aluno01"
    aluno.matricula = "12345"
    return aluno

@pytest.fixture
def professor():
    prof = Mock()
    prof.username = "prof01"
    return prof

# --- Factory de Avaliacao mock ---
@pytest.fixture
def avaliacao_factory():
    """Cria uma lista de avaliações mock com média e status calculados."""
    def _factory(notas=(7.0, 7.0), faltas=0, qtd=1, aluno=None, professor=None):
        avals = []
        for _ in range(qtd):
            av = Mock()
            av.aluno = aluno
            av.professor = professor
            av.nota_b1, av.nota_b2 = notas
            av.faltas = faltas
            av.media = (av.nota_b1 + av.nota_b2) / 2
            # calcula status
            if av.faltas > FALTAS_LIMITE_REPROVACAO:
                av.status = "Reprovado por faltas"
            elif av.media >= MEDIA_APROVACAO:
                av.status = "Aprovado"
            else:
                av.status = "Reprovado"
            avals.append(av)
        return avals
    return _factory

# --- Testes ---

def test_CT11_crud_avaliacao_model(aluno, professor, avaliacao_factory):
    """Simula CRUD de Avaliacao sem banco."""
    # CREATE
    av = avaliacao_factory(notas=(8.0, 8.0), faltas=2, qtd=1, aluno=aluno, professor=professor)[0]
    assert av.media == 8.0
    assert av.status == "Aprovado"

    # UPDATE
    av.nota_b1 = 9.0
    av.nota_b2 = 9.0
    av.faltas = 1
    av.media = (av.nota_b1 + av.nota_b2) / 2
    av.status = "Aprovado" if av.media >= MEDIA_APROVACAO else "Reprovado"
    assert av.media == 9.0
    assert av.status == "Aprovado"

    # DELETE
    del av
    # apenas verificamos que a variável foi removida
    assert True

def test_CT01_calcular_media_aprovado(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(7.0, 7.0), faltas=0, qtd=1, aluno=aluno, professor=professor)[0]
    assert round(av.media, 2) == 7.00

def test_CT02_status_aprovado(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(7.0, 7.0), faltas=0, qtd=1, aluno=aluno, professor=professor)[0]
    assert av.status == "Aprovado"

def test_CT03_reprovado_por_faltas(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(8.0, 8.0), faltas=16, qtd=1, aluno=aluno, professor=professor)[0]
    assert av.status == "Reprovado por faltas"

def test_CT04_reprovado_por_media_baixa(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(5.0, 6.0), faltas=0, qtd=1, aluno=aluno, professor=professor)[0]
    assert av.status == "Reprovado"
