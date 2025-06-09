"""
Professores cadastram avaliações: notas do 1º e 2º bimestre + faltas.
O sistema calcula automaticamente a média e o status (ex: média >= 6 e faltas <= 10 = aprovado).
Alunos (usuários comuns) podem acessar suas informações com login e senha.
"""
from django.db import models
from django.contrib.auth.models import User

# Classe que representa um aluno no sistema
class Aluno(models.Model):
    # Relacionamento com o usuário do sistema
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Número de matrícula único do aluno
    matricula = models.CharField(
    max_length=20,
    unique=True,
    error_messages={
        'unique': "Matrícula já cadastrada. Use uma diferente."
    }
)

    # Retorna o nome completo do aluno
    def __str__(self):
        return self.user.get_full_name()
    
# Classe que representa um professor no sistema
class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Retorna o nome completo do professor
    def __str__(self):
        return self.user.get_full_name()
    
# Classe que representa as avaliações dos alunos
class Avaliacao(models.Model):
    # Aluno que está sendo avaliado
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    # Professor que está fazendo a avaliação
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    # Notas
    nota_b1 = models.FloatField()
    nota_b2 = models.FloatField()
    # Faltas
    faltas = models.PositiveIntegerField(default=0)
    
    # Status do aluno
    STATUS_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
    ]
    # Status atual do aluno 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)

    @property
    def media(self):
        return round((self.nota_b1 + self.nota_b2) / 2, 2)


    # Aprovado se média >= 6 e faltas <= 10
    def calcular_status(self):
        media = self.media  
        if self.faltas > 15:
            return 'Reprovado por faltas'
        elif media >= 7.0:
            return 'Aprovado'
        else:
            return 'Reprovado'


    # Salva a avaliação e atualiza o status automaticamente
    def save(self, *args, **kwargs):
        self.status = self.calcular_status()
        super().save(*args, **kwargs)

    # Retorna uma string com informações da avaliação
    def __str__(self):
        return f"{self.aluno} - Média: {self.media} - {self.status}"

    