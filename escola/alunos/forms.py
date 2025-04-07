# alunos/forms.py
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Avaliacao, Aluno, Professor

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['aluno', 'nota_b1', 'nota_b2', 'faltas']
        widgets = {
            'nota_b1': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.1}),
            'nota_b2': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.1}),
            'faltas': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_nota_b1(self):
        nota = self.cleaned_data['nota_b1']
        if not 0 <= nota <= 10:
            raise forms.ValidationError('A nota deve estar entre 0 e 10')
        return nota

    def clean_nota_b2(self):
        nota = self.cleaned_data['nota_b2']
        if not 0 <= nota <= 10:
            raise forms.ValidationError('A nota deve estar entre 0 e 10')
        return nota

    def clean_faltas(self):
        faltas = self.cleaned_data['faltas']
        if faltas < 0:
            raise forms.ValidationError('O número de faltas não pode ser negativo')
        return faltas

from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Senha',
        help_text='A senha deve ter pelo menos 8 caracteres, incluindo letras e números'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar Senha'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('A senha deve ter pelo menos 8 caracteres')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('A senha deve conter pelo menos um número')
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem')
        return cleaned_data

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['matricula']
        help_texts = {
            'matricula': 'A matrícula deve ter 8 dígitos numéricos'
        }

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if not matricula.isdigit() or len(matricula) != 8:
            raise forms.ValidationError('A matrícula deve conter exatamente 8 dígitos numéricos')
        return matricula

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = []  # Nenhum campo extra além do user
