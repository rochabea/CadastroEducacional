
from django.urls import path
from . import views
from .views import MeusFeedbacksView, FeedbackCreateView, MeusFeedbacksProfessorView

urlpatterns = [
    # Rota inicial do sistema
    path('', views.login_view, name='login'),
    
    # Rotas de autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Rotas do painel de controle
    path('dashboard/professor/', views.dashboard_professor, name='dashboard_professor'),
    path('dashboard/aluno/', views.dashboard_aluno, name='dashboard_aluno'),
    
    # Rotas de gerenciamento de avaliações
    path('professor/lancar/', views.lancar_avaliacao, name='lancar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),
    
    # Rota do boletim do aluno
    path('aluno/boletim/', views.boletim_aluno, name='boletim_aluno'),
    
    # Rotas de cadastro
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),

    # Rota para visualização das avaliações
    path('avaliacoes/lista/', views.lista_avaliacoes, name='lista_avaliacoes'),
    path('avaliacoes/consulta/', views.consulta_avaliacoes, name='consulta_avaliacoes'),

    #Rota para exportar o pdf
<<<<<<< HEAD
    path('exportar-pdf/', views.gerar_os, name="exportar_pdf"),

    #Rota para acessar a página de feedback
    #path('dashboard/feedback/', views.feedback_view, name='feedback_view'),

    #Rota para acessar a página de presença de alunos
    path('dashboard/presenca_alunos/', views.presenca_alunos, name='presenca_alunos'),

    #Rota para acessar a página de presença de professores
    path('dashboard/presenca_professor/', views.presenca_professor_view, name='presenca_professor'),
    
    #Rota para acessar a página de quadro de horários
    path('dashboard/quadro_horario/', views.quadro_view, name='quadro_view'),

    path('dashboard/quadro_horario_aluno/', views.quadro_aluno_view, name='quadro_aluno_view'),

    path('dashboard/cadastrar_turma/', views.cadastrar_turma_view, name='cadastrar_turma_view'),

    # Rotas de feedback
    path('aluno/feedbacks/', MeusFeedbacksView.as_view(), name='aluno-meus-feedbacks'),
    path('professor/feedbacks/novo/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('professor/feedbacks/', MeusFeedbacksProfessorView.as_view(), name='prof-meus-feedbacks'),

    path('dashboard/perfil_view', views.perfil_view, name='perfil_view'),

    
=======
    path('exportar-pdf/', views.gerar_os, name="exportar_pdf")

>>>>>>> 63ce42e234d66c938219ed3b899adda601aa622b
]