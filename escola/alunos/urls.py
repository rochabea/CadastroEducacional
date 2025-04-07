from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/professor/', views.dashboard_professor, name='dashboard_professor'),
    path('dashboard/aluno/', views.dashboard_aluno, name='dashboard_aluno'),
    path('professor/lancar/', views.lancar_avaliacao, name='lancar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),
    path('aluno/boletim/', views.boletim_aluno, name='boletim_aluno'),
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),
]