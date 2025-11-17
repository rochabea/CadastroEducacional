# tests/conftest.py
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from model_bakery import baker
import sys, types

# --- STUB PARA 'fpdf' EM AMBIENTE DE TESTE
if "fpdf" not in sys.modules:
    fake_fpdf = types.ModuleType("fpdf")

    class FPDF:
        def __init__(self, *args, **kwargs): pass
        def add_page(self): pass
        def set_font(self, *args, **kwargs): pass
        def cell(self, *args, **kwargs): pass
        def ln(self, *args, **kwargs): pass
        def output(self, dest=None): return "PDF"

    fake_fpdf.FPDF = FPDF
    sys.modules["fpdf"] = fake_fpdf

# --- DATABASE MOCK: SQLite em memória

@pytest.fixture(autouse=True)
def override_db_settings(settings):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {'check_same_thread': False},
    }
    
@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {'check_same_thread': False},
    }

# --- FIXTURES DE USUÁRIOS E MODELOS
@pytest.fixture
def user_staff(db):
    User = get_user_model()
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
    return baker.make("alunos.Aluno", user=user_aluno)

@pytest.fixture
def disciplina(db):
    return baker.make("alunos.Disciplina", nome="matematica")

@pytest.fixture
def avaliacao_factory(db, aluno, professor):
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
