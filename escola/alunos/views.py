from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Avaliacao, Aluno, Professor
from .forms import AvaliacaoForm, UserForm, AlunoForm, ProfessorForm

# Página inicial do sistema
def home(request):
    return render(request, 'home.html')

# Painel de controle do professor
@login_required
def dashboard_professor(request):
    try:
        professor = Professor.objects.get(user=request.user)
        avaliacoes = (Avaliacao.objects
                     .filter(professor=professor)
                     .select_related('aluno', 'aluno__user')
                     .order_by('aluno__user__first_name', 'aluno__user__last_name'))
        return render(request, 'alunos/dashboard_professor.html', {'avaliacoes': avaliacoes})
    except Professor.DoesNotExist:
        return redirect('home')

# Permite ao professor lançar uma nova avaliação
@login_required
def lancar_avaliacao(request):
    try:
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
    except Professor.DoesNotExist:
        return redirect('home')

# Mostra o boletim do aluno com suas notas e faltas
@login_required
def boletim_aluno(request):
    try:
        aluno = Aluno.objects.get(user=request.user)
        avaliacoes = Avaliacao.objects.filter(aluno=aluno).select_related('professor', 'professor__user')

        boletim = []
        for avaliacao in avaliacoes:
            boletim.append({
                'professor': avaliacao.professor.user.get_full_name(),
                'nota_b1': avaliacao.nota_b1,
                'nota_b2': avaliacao.nota_b2,
                'media': avaliacao.media,
                'status': avaliacao.status,
                'faltas': avaliacao.faltas,
            })

        return render(request, 'alunos/boletim_aluno.html', {
            'boletim': boletim,
            'aluno': aluno
        })
    except Aluno.DoesNotExist:
        messages.error(request, 'Aluno não encontrado')
        return render(request, 'error.html', {'message': 'Aluno não encontrado'})



def calcular_media(nota1, nota2):
    if nota1 is not None and nota2 is not None:
        return round((nota1 + nota2) / 2, 1)
    return None


# Painel de controle do aluno
@login_required
def dashboard_aluno(request):
    try:
        aluno = Aluno.objects.get(user=request.user)
        avaliacoes = Avaliacao.objects.filter(aluno=aluno)
        return render(request, 'alunos/dashboard_aluno.html', {'avaliacoes': avaliacoes})
    except Aluno.DoesNotExist:
        messages.error(request, 'Aluno não encontrado')
        return render(request, 'error.html', {'message': 'Aluno não encontrado'})

# Permite o cadastro de um novo aluno no sistema
def cadastro_aluno(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        aluno_form = AlunoForm(request.POST)
        if user_form.is_valid() and aluno_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            aluno = aluno_form.save(commit=False)
            aluno.user = user
            aluno.save()
            messages.success(request, 'Aluno cadastrado com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        user_form = UserForm()
        aluno_form = AlunoForm()
    return render(request, 'cadastro_aluno.html', {
        'user_form': user_form,
        'aluno_form': aluno_form
    })

# Permite o cadastro de um novo professor no sistema
def cadastro_professor(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        prof_form = ProfessorForm(request.POST)
        if user_form.is_valid() and prof_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            professor = prof_form.save(commit=False)
            professor.user = user
            professor.save()
            messages.success(request, 'Professor cadastrado com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        user_form = UserForm()
        prof_form = ProfessorForm()
    return render(request, 'cadastro_professor.html', {
        'user_form': user_form,
        'prof_form': prof_form
    })

# Gerencia o processo de login dos usuários
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            try:
                professor = Professor.objects.get(user=user)
                return redirect('dashboard_professor')
            except Professor.DoesNotExist:
                try:
                    aluno = Aluno.objects.get(user=user)
                    return redirect('dashboard_aluno')
                except Aluno.DoesNotExist:
                    return redirect('login')
        else:
            return redirect('login')
    
    return render(request, 'login.html')

# Permite ao professor editar uma avaliação existente
@login_required
def editar_avaliacao(request, avaliacao_id):
    try:
        professor = Professor.objects.get(user=request.user)
        avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id, professor=professor)
        
        if request.method == 'POST':
            form = AvaliacaoForm(request.POST, instance=avaliacao)
            if form.is_valid():
                form.save()
                messages.success(request, 'Avaliação atualizada com sucesso!')
                return redirect('dashboard_professor')
            else:
                messages.error(request, 'Por favor, corrija os erros no formulário.')
        else:
            form = AvaliacaoForm(instance=avaliacao)
            
        return render(request, 'alunos/lancar_avaliacao.html', {
            'form': form,
            'avaliacao': avaliacao,
            'editar': True
        })
    except Professor.DoesNotExist:
        messages.error(request, 'Professor não encontrado')
        return render(request, 'error.html', {'message': 'Professor não encontrado'})

# Permite ao professor excluir uma avaliação
@login_required
def excluir_avaliacao(request, avaliacao_id):
    try:
        professor = Professor.objects.get(user=request.user)
        avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id, professor=professor)
        
        if request.method == 'POST':
            avaliacao.delete()
            messages.success(request, 'Avaliação excluída com sucesso!')
            return redirect('dashboard_professor')
            
        return render(request, 'alunos/confirmar_exclusao.html', {
            'avaliacao': avaliacao
        })
    except Professor.DoesNotExist:
        messages.error(request, 'Professor não encontrado')
        return render(request, 'error.html', {'message': 'Professor não encontrado'})

# Gerencia o processo de logout dos usuários
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout.html')



