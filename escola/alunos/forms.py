from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Avaliacao, Aluno, Professor
from django.contrib.auth.models import User

# Formulário para cadastro de usuários (alunos e professores)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }

# Formulário para cadastro de alunos
class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['matricula']
        help_texts = {
            'matricula': 'A matrícula deve ter 8 dígitos numéricos'
        }

    # Valida se a matrícula contém exatamente 8 dígitos numéricos
    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if not matricula.isdigit() or len(matricula) != 8:
            raise forms.ValidationError('A matrícula deve conter exatamente 8 dígitos numéricos')
        return matricula

# Formulário para cadastro de professores
class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = []

# Formulário para lançamento de avaliações
class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['aluno', 'nota_b1', 'nota_b2', 'faltas']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'nota_b1': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.1, 'class': 'form-control'}),
            'nota_b2': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.1, 'class': 'form-control'}),
            'faltas': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
        }

    # Valida se a nota do primeiro bimestre está entre 0 e 10
    def clean_nota_b1(self):
        nota = self.cleaned_data.get('nota_b1')
        if nota is not None and not 0 <= nota <= 10:
            raise forms.ValidationError('A nota deve estar entre 0 e 10')
        return nota

    # Valida se a nota do segundo bimestre está entre 0 e 10
    def clean_nota_b2(self):
        nota = self.cleaned_data.get('nota_b2')
        if nota is not None and not 0 <= nota <= 10:
            raise forms.ValidationError('A nota deve estar entre 0 e 10')
        return nota

    # Valida se o número de faltas não é negativo
    def clean_faltas(self):
        faltas = self.cleaned_data.get('faltas')
        if faltas is not None and faltas < 0:
            raise forms.ValidationError('O número de faltas não pode ser negativo')
        return faltas
