
from django.urls import path
from . import views

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
    path('exportar-pdf/', views.gerar_os, name="exportar_pdf")

]