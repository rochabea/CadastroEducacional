"""
Professores cadastram avaliações: notas do 1º e 2º bimestre + faltas.
O sistema calcula automaticamente a média e o status (ex: média >= 6 e faltas <= 10 = aprovado).
Alunos (usuários comuns) podem acessar suas informações com login e senha.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Horario(models.Model):
    hora = models.TimeField()

    def __str__(self):
        return self.hora.strftime("%H:%M")


class Aula(models.Model):
    DIAS_SEMANA = [
        ("segunda", "Segunda"),
        ("terca", "Terça"),
        ("quarta", "Quarta"),
        ("quinta", "Quinta"),
        ("sexta", "Sexta"),
    ]

    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name="aulas")
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    disciplina = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_dia_display()} - {self.disciplina}"

class Presenca(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('aluno', 'disciplina', 'data')
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Classe que representa um aluno no sistema
class Aluno(models.Model):
    disciplinas = models.ManyToManyField(Disciplina, related_name='alunos', blank=True)
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

    # Verifica se as notas estão dentro do intervalo válido
    def clean(self):
        if not (0 <= self.nota_b1 <= 10):
            raise ValidationError("Nota B1 inválida: deve estar entre 0 e 10.")
        if not (0 <= self.nota_b2 <= 10):
            raise ValidationError("Nota B2 inválida: deve estar entre 0 e 10.")
        

# classe feedback do professor para o aluno
class Feedback(models.Model):
    # se um aluno for remevido todos os feedbacks dele serão removidos -> CASCADE
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='feedbacks')
    # se um professor for removido, o feedback permanece, mas o campo professor fica nulo -> SET_NULL
    # related_name -> acessar todos os feedbacjs criados por esse professor
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    # campo de texto do feedback
    texto = models.TextField()
    # campo para indicar se o feedback é visível para o aluno
    visivel_para_aluno = models.BooleanField(default=True)
    # data e hora em que o feedback foi criado automaticamente
    criado_em = models.DateTimeField(auto_now_add=True)
    # data e hora da última atualização
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta:
        # ordena pelo mais recente
        ordering = ['-criado_em']
        # índice no bd para otimizar consultas por aluno e data de criação
        indexes = [models.Index(fields=['aluno', '-criado_em'])]

    # representação legível no admin e nos logs
    def __str__(self):
        return f'Feedback para {self.aluno} por {getattr(self.professor, "nome", "—")}'        