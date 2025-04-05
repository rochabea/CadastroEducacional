# alunos/forms.py
from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['aluno', 'nota_b1', 'nota_b2', 'faltas']
