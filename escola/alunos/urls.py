from django.urls import path
from . import views

urlpatterns = [
    path('professor/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/lancar/', views.lancar_avaliacao, name='lancar_avaliacao'),
    path('aluno/', views.boletim_aluno, name='boletim_aluno'),
]