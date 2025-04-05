'''
Professores cadastram avaliações: notas do 1º e 2º bimestre + faltas.
O sistema calcula automaticamente a média e o status (ex: média >= 6 e faltas <= 10 = aprovado).
Alunos (usuários comuns) podem acessar suas informações com login e senha.


from django.db import models
from django.contrib.auth.models import User

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.get_full_name()
    
class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
    
class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    nota_b1 = models.FloatField()
    nota_b2 = models.FloatField()
    faltas = models.PositiveBigIntegerField(default=0)

    STATUS_CHOICE = [
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICE, blank=True)

    def media(self):
        # round está arredondando o numero para duas casas decimais
        return round((self.nota_b1 + self.nota_b2)/2,2)

    def calcular_status(self):
        media = self.media()
        # definindo a nota e a quantidade de faltas para o aluno ser aprovado/reprovado
        return 'Aprovado' if media >= 6 and self.faltas <= 10 else 'Reprovado'
    
    def save(self, *args, **kwargs):
        self.status = self.calcular_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.aluno} - {self.media()} : {self.status}"
    
    '''
# alunos/models.py
from django.db import models
from django.contrib.auth.models import User

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.get_full_name()

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    nota_b1 = models.FloatField()
    nota_b2 = models.FloatField()
    faltas = models.PositiveIntegerField(default=0)
    
    STATUS_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)

    def media(self):
        return round((self.nota_b1 + self.nota_b2) / 2, 2)

    def calcular_status(self):
        media = self.media()
        return 'Aprovado' if media >= 6 and self.faltas <= 10 else 'Reprovado'

    def save(self, *args, **kwargs):
        self.status = self.calcular_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.aluno} - Média: {self.media()} - {self.status}"
