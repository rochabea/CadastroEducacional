# tests/test_avaliacoes_integration.py
import pytest
from django.db.models import Avg, Sum

MEDIA_APROVACAO = 7.0
FALTAS_LIMITE_REPROVACAO = 15  # seu model reprova se faltas > 15

@pytest.mark.django_db
def test_CT11_crud_avaliacao_model(db, aluno, professor):
    from alunos.models import Avaliacao

    # CREATE
    av = Avaliacao.objects.create(
        aluno=aluno, professor=professor, nota_b1=8.0, nota_b2=8.0, faltas=2
    )
    assert av.id is not None
    assert av.media == 8.0
    assert av.status == "Aprovado"  # média 8 e faltas 2 -> aprovado

    # READ (lista e agregações)
    qs = Avaliacao.objects.filter(aluno=aluno)
    assert qs.count() == 1
    media_calc = qs.aggregate(m=Avg((1.0*0)+(1.0*0)))  # dummy para manter padrão
    # forma direta: usar propriedade do obj ou recalc:
    assert float(qs.first().media) == 8.0

    # UPDATE
    av.nota_b1 = 9.0
    av.nota_b2 = 9.0
    av.faltas = 1
    av.save()
    av.refresh_from_db()
    assert av.media == 9.0
    assert av.status == "Aprovado"

    # DELETE
    pk = av.pk
    av.delete()
    assert not Avaliacao.objects.filter(pk=pk).exists()

@pytest.mark.django_db
def test_CT01_calcular_media_aprovado(aluno, professor, avaliacao_factory):
    # duas avaliações não são necessárias neste modelo (você já guarda b1 e b2),
    # mas manteremos a ideia de "média 7" em uma única Avaliacao
    objs = avaliacao_factory(notas=(7.0, 7.0), faltas=0, qtd=1)
    av = objs[0]
    assert round(float(av.media), 2) == 7.00

@pytest.mark.django_db
def test_CT02_status_aprovado(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(7.0, 7.0), faltas=0, qtd=1)[0]
    # regra do seu model: média >= 7.0 e faltas <= 15 => "Aprovado"
    assert av.status == "Aprovado"

@pytest.mark.django_db
def test_CT03_reprovado_por_faltas(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(8.0, 8.0), faltas=16, qtd=1)[0]
    # seu calcular_status retorna "Reprovado por faltas" se faltas > 15
    assert av.status == "Reprovado por faltas"

@pytest.mark.django_db
def test_CT04_reprovado_por_media_baixa(aluno, professor, avaliacao_factory):
    av = avaliacao_factory(notas=(5.0, 6.0), faltas=0, qtd=1)[0]
    assert av.status == "Reprovado"
