from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Treinamento(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Treinamento'
        verbose_name_plural = 'Treinamentos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome


class Turma(models.Model):
    treinamento = models.ForeignKey(
        Treinamento, 
        on_delete=models.CASCADE,
        related_name='turmas'
    )
    nome = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_conclusao = models.DateField()
    link_acesso = models.URLField(max_length=500, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.nome} - {self.treinamento.nome}"


class Recurso(models.Model):
    TIPO_CHOICES = [
        ('video', 'Vídeo'),
        ('pdf', 'Arquivo PDF'),
        ('zip', 'Arquivo ZIP'),
    ]

    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='recursos'
    )
    tipo_recurso = models.CharField(max_length=10, choices=TIPO_CHOICES)
    acesso_previo = models.BooleanField(
        default=False,
        help_text='Permite acesso antes da data de início'
    )
    draft = models.BooleanField(
        default=False,
        help_text='Recurso em rascunho (não visível para alunos)'
    )
    nome_recurso = models.CharField(max_length=200)
    descricao_recurso = models.TextField()
    arquivo = models.FileField(
        upload_to='recursos/%Y/%m/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp4', 'avi', 'mov', 'pdf', 'zip']
            )
        ],
        blank=True,
        null=True
    )
    url_recurso = models.URLField(max_length=500, blank=True, null=True)
    ordem = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['ordem', '-criado_em']

    def __str__(self):
        return f"{self.nome_recurso} ({self.get_tipo_recurso_display()})"


class Aluno(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='aluno'
    )
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Matricula(models.Model):
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='matriculas'
    )
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='matriculas'
    )
    data_matricula = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ['turma', 'aluno']
        ordering = ['-data_matricula']

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"