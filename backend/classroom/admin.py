from django.contrib import admin
from .models import Treinamento, Turma, Recurso, Aluno, Matricula


@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado_em']
    search_fields = ['nome', 'descricao']
    list_filter = ['criado_em']
    date_hierarchy = 'criado_em'


class RecursoInline(admin.TabularInline):
    model = Recurso
    extra = 1
    fields = ['nome_recurso', 'tipo_recurso', 'acesso_previo', 'draft', 'ordem']


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'treinamento', 'data_inicio', 'data_conclusao', 'total_matriculas']
    search_fields = ['nome', 'treinamento__nome']
    list_filter = ['treinamento', 'data_inicio']
    date_hierarchy = 'data_inicio'
    inlines = [RecursoInline]
    
    def total_matriculas(self, obj):
        return obj.matriculas.filter(ativo=True).count()
    total_matriculas.short_description = 'Alunos Matriculados'


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ['nome_recurso', 'turma', 'tipo_recurso', 'acesso_previo', 'draft', 'ordem']
    search_fields = ['nome_recurso', 'descricao_recurso']
    list_filter = ['tipo_recurso', 'acesso_previo', 'draft', 'turma']
    list_editable = ['ordem', 'acesso_previo', 'draft']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'username', 'criado_em']
    search_fields = ['nome', 'email', 'user__username']
    list_filter = ['criado_em']
    date_hierarchy = 'criado_em'
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'turma', 'treinamento', 'data_matricula', 'ativo']
    search_fields = ['aluno__nome', 'turma__nome']
    list_filter = ['ativo', 'turma__treinamento', 'data_matricula']
    date_hierarchy = 'data_matricula'
    list_editable = ['ativo']
    
    def treinamento(self, obj):
        return obj.turma.treinamento.nome
    treinamento.short_description = 'Treinamento'