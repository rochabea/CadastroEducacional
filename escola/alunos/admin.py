from django.contrib import admin
from .models import Aluno, Professor,Feedback

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    # busca pelo usuário vinculado e pela matrícula
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'matricula',
    )
    list_display = ('id', 'user', 'matricula')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
    )
    list_display = ('id', 'user')

# Registro do modelo Feedback no admin do Django
@admin.register(Feedback)
# define como o modelo Feedback será exibido e manipulado no admin
class FeedbackAdmin(admin.ModelAdmin):
    # define as colunas exibidas na lista de Feedbacks dentro do admin
    list_display = ('aluno', 'professor', 'visivel_para_aluno', 'criado_em')
    # adicona filtros laterais para facilitar a busca
    list_filter  = ('visivel_para_aluno', 'professor')
    # habilita a busca por texto e nomes relacionados
    search_fields = (
        'texto',
        'aluno__user__username',
        'aluno__user__first_name',
        'aluno__user__last_name',
        'aluno__user__email',
        'professor__user__username',
        'professor__user__first_name',
        'professor__user__last_name',
        'professor__user__email',             # busca pelo nome do professor
    )
    # altera para campos de autocomplete
    autocomplete_fields = ('aluno', 'professor')
    # define a ordem padrão dos feedbacks pela data de criação (mais recentes primeiro)
    ordering = ('-criado_em',)