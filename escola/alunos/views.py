# alunos/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Avaliacao, Aluno, Professor
from .forms import AvaliacaoForm

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard_professor(request):
    professor = Professor.objects.get(user=request.user)
    avaliacoes = Avaliacao.objects.filter(professor=professor)
    return render(request, 'alunos/dashboard_professor.html', {'avaliacoes': avaliacoes})

@login_required
def lancar_avaliacao(request):
    professor = Professor.objects.get(user=request.user)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.professor = professor
            avaliacao.save()
            return redirect('dashboard_professor')
    else:
        form = AvaliacaoForm()
    return render(request, 'alunos/lancar_avaliacao.html', {'form': form})

@login_required
def boletim_aluno(request):
    aluno = Aluno.objects.get(user=request.user)
    avaliacoes = Avaliacao.objects.filter(aluno=aluno)
    return render(request, 'alunos/boletim_aluno.html', {'avaliacoes': avaliacoes})
