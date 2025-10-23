from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Avaliacao, Aluno, Professor, Feedback
from .forms import AvaliacaoForm, UserForm, AlunoForm, ProfessorForm
from fpdf import FPDF

# Página inicial do sistema
def home(request):
    return render(request, 'login.html')

# Painel de controle do professor
@login_required
def dashboard_professor(request):
    try:
        professor = Professor.objects.get(user=request.user)
        avaliacoes = (Avaliacao.objects
                     .filter(professor=professor)
                     .select_related('aluno', 'aluno__user')
                     .order_by('aluno__user__first_name', 'aluno__user__last_name'))
        total_alunos = Aluno.objects.count()
        total_aprovados = avaliacoes.filter(status="Aprovado").count()
        total_reprovados = avaliacoes.filter(status="Reprovado").count()

        medias = [a.media for a in avaliacoes if a.media is not None]
        media_geral = round(sum(medias) / len(medias), 1) if medias else 0

        alunos = Aluno.objects.select_related("user").all().order_by("user__first_name", "user__last_name")

        return render(request, 'alunos/dashboard_professor.html', 
               {'avaliacoes': avaliacoes,
                'total_alunos': total_alunos,
                'total_aprovados': total_aprovados,
                'total_reprovados': total_reprovados,
                'media_geral': media_geral,
                'alunos' : alunos})
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


#função para exportar o pdf
@login_required
def gerar_os(request):
    #cria o PDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    #título do pdf
    pdf.cell(200,10, txt="Boletim", ln=True, align="C")

    #busca de dados
    avaliacoes = Avaliacao.objects.all()

    pdf.ln(10)

    #cabecalho
    pdf.set_font("Arial", style="B",size=12)
    pdf.cell(60,10, "Aluno", 1)
    pdf.cell(40,10, "Média", 1)
    pdf.cell(40,10, "Status", 1)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    for avaliacao in avaliacoes:
        pdf.cell(60,10, str(avaliacao.aluno), 1)
        pdf.cell(40,10, str(avaliacao.media), 1)
        pdf.cell(40,10, str(avaliacao.status), 1)
        pdf.ln()

    #retorno de pdf
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="notas.pdf"'
    return response



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

def lista_avaliacoes(request):
    # Retorno simples para os testes funcionarem
    return HttpResponse("Lista de avaliações")

#def feedback_view(request):
#    return render(request, 'alunos/feedback.html')

def presenca_alunos(request):
    return render(request, 'alunos/presenca_alunos.html')

def cadastrar_turma_view(request):
    return render(request, 'alunos/cadastrar_turma.html')

@login_required
def consulta_avaliacoes(request):
    try:
        aluno = Aluno.objects.get(user=request.user)
        avaliacoes = Avaliacao.objects.filter(aluno=aluno)
        return render(request, 'alunos/consulta_avaliacoes.html', {'avaliacoes': avaliacoes})
    except Aluno.DoesNotExist:
        messages.error(request, 'Aluno não encontrado')
        return render(request, 'error.html', {'message': 'Aluno não encontrado'})

def presenca_professor_view(request):
    # Dados de exemplo
    registros = [
        {"id": 1, "aluno": "João Silva", "disciplina": "POO", "data": "11/10/2025", "presente": True},
        {"id": 2, "aluno": "Maria Souza", "disciplina": "Processo de Negócios", "data": "10/10/2025", "presente": False},
        {"id": 3, "aluno": "Carlos Pereira", "disciplina": "Banco de Dados", "data": "09/10/2025", "presente": True},
        {"id": 4, "aluno": "Ana Costa", "disciplina": "Algoritmos", "data": "12/10/2025", "presente": True},
        {"id": 5, "aluno": "Rafael Lima", "disciplina": "Engenharia de Software", "data": "08/10/2025", "presente": False},
        {"id": 6, "aluno": "Fernanda Oliveira", "disciplina": "Redes de Computadores", "data": "07/10/2025", "presente": True},
    ]

    # Pega disciplina selecionada no filtro (GET)
    disciplina_filtro = request.GET.get('disciplina', 'todas')

    # Lista de disciplinas únicas
    disciplinas_unicas = sorted(set(r['disciplina'] for r in registros))

    # Filtra registros se a disciplina não for "todas"
    if disciplina_filtro != 'todas':
        registros = [r for r in registros if r['disciplina'] == disciplina_filtro]

    return render(request, 'alunos/presenca_professor.html', {
        "registros": registros,
        "disciplinas": disciplinas_unicas,
        "disciplina_filtro": disciplina_filtro,
    })

def quadro_view(request):
    # Horários fixos com 3 fileiras cada e matérias de T.I.
    horarios = [
        {"hora": "08:00", "aulas": ["Programação", "Banco de Dados", "Redes"]},
        {"hora": "10:00", "aulas": ["Sistemas Operacionais", "Engenharia de Software", "Segurança da Informação"]},
        {"hora": "12:00", "aulas": ["Desenvolvimento Web", "Inteligência Artificial", "Arquitetura de Computadores"]},
    ]

    context = {
        "horarios": horarios
    }
    return render(request, 'alunos/quadro_horario.html', context)

# Gerencia o processo de logout dos usuários
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'login.html')

# Aluno vê os próprios feedbacks -> apenas usuários autenticados acessam a página
class MeusFeedbacksView(LoginRequiredMixin, ListView):
    # indica a tabela
    model = Feedback
    # qual template usar
    template_name = 'alunos/meus_feedbacks.html'
    # nome da variável no template
    context_object_name = 'feedbacks'
    # nº de itens por página
    paginate_by = 10

    def get_queryset(self):
        # user -> aluno
        if hasattr(self.request.user, 'aluno'):
            # se for aluno retorna apenas o feedback dele e os vísiveis para ele
            return (Feedback.objects
                    .filter(aluno=self.request.user.aluno, visivel_para_aluno=True)
                    # join com o banco para tarzer o porfessor e o user do professor (reduzir queries)
                    .select_related('professor__user')
                    # ordem dos mais novas para os mais antigos
                    .order_by('-criado_em'))
        return Feedback.objects.none()

# Professor cria feedback (fora do admin) 
class ProfessorRequiredMixin(UserPassesTestMixin):
    # apenas quem tem relação: user -> professor
    def test_func(self):
        return hasattr(self.request.user, 'professor')

    # em caso de erro, não irá redirecionar mas lançar um 403
    def handle_no_permission(self):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Apenas professores podem acessar esta página.")

# para onde redirecionar swpoisa de salvar (lista do professor)
class FeedbackCreateView(LoginRequiredMixin, ProfessorRequiredMixin, CreateView):
    model = Feedback
    fields = ['aluno', 'texto', 'visivel_para_aluno']   # professor é setado no form_valid
    template_name = 'alunos/feedback_create.html'
    success_url = reverse_lazy('prof-meus-feedbacks')

    # força o vínculo do feedback ao professor logado
    def form_valid(self, form):
        form.instance.professor = self.request.user.professor
        # Regra: restringir alunos que este professor pode avaliar.
        return super().form_valid(form)

# Professor lista o que ele criou 
class MeusFeedbacksProfessorView(LoginRequiredMixin, ProfessorRequiredMixin, ListView):
    model = Feedback
    template_name = 'alunos/meus_feedbacks_prof.html'
    context_object_name = 'feedbacks'
    paginate_by = 10
    # lista apenas os feedbacks criados por esse professor
    def get_queryset(self):
        return (Feedback.objects
                .filter(professor=self.request.user.professor)
                # otimiza as queries trazendo aluno e user do aluno
                .select_related('aluno__user')
                .order_by('-criado_em'))




