# tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

@pytest.fixture
def user_staff(db):
    User = get_user_model()
    # staff pode ser também o professor
    return User.objects.create_user(
        username="staff",
        password="SenhaForte123!",
        is_staff=True,
        is_superuser=True,
        first_name="Profe",
        last_name="Staff",
        email="staff@example.com",
    )

@pytest.fixture
def professor(db, user_staff):
    # Professor é OneToOne com User
    return baker.make("alunos.Professor", user=user_staff)

@pytest.fixture
def user_aluno(db):
    User = get_user_model()
    return User.objects.create_user(
        username="aluno1",
        password="SenhaForte123!",
        first_name="Aluno",
        last_name="Teste",
        email="aluno1@example.com",
    )

@pytest.fixture
def aluno(db, user_aluno):
    # Aluno é OneToOne com User
    return baker.make("alunos.Aluno", user=user_aluno)

@pytest.fixture
def disciplina(db):
    return baker.make("alunos.Disciplina", nome="Matemática")

@pytest.fixture
def avaliacao_factory(db, aluno, professor):
    """
    Cria avaliações para (aluno, professor) aceitando tupla de notas (b1,b2) e faltas.
    Uso: avaliacao_factory(notas=(7.0, 8.0), faltas=2, qtd=1)
    """
    from alunos.models import Avaliacao

    def _factory(notas=(7.0, 7.0), faltas=0, qtd=1):
        objs = []
        nota_b1, nota_b2 = notas
        for _ in range(qtd):
            objs.append(
                Avaliacao.objects.create(
                    aluno=aluno,
                    professor=professor,
                    nota_b1=nota_b1,
                    nota_b2=nota_b2,
                    faltas=faltas,
                )
            )
        return objs

    return _factory
