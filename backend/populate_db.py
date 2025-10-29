import os
import django
from django.contrib.auth.models import User
from classroom.models import Treinamento, Turma, Recurso, Aluno, Matricula
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classroom_project.settings')
django.setup()

print("Iniciando populacao do banco de dados...")

# Limpar dados existentes
print("Limpando dados antigos...")
Matricula.objects.all().delete()
Recurso.objects.all().delete()
Turma.objects.all().delete()
Treinamento.objects.all().delete()
Aluno.objects.filter(user__is_staff=False).delete()
User.objects.filter(is_staff=False).delete()

# Criar Treinamentos
treinamentos = [
    Treinamento.objects.create(nome="Python para Iniciantes", descricao="Aprenda Python do zero"),
    Treinamento.objects.create(nome="Django e DRF Avancado", descricao="Desenvolvimento de APIs REST"),
    Treinamento.objects.create(nome="React Moderno", descricao="Aplicacoes web modernas com React"),
]
print(f"{len(treinamentos)} treinamentos criados")

# Criar Turmas
hoje = date.today()
turmas = [
    Turma.objects.create(treinamento=treinamentos[0], nome="Python Iniciantes - Jan 2026",
                        data_inicio=hoje + timedelta(days=60), data_conclusao=hoje + timedelta(days=150),
                        link_acesso="https://zoom.us/j/111111"),
    Turma.objects.create(treinamento=treinamentos[1], nome="Django DRF - Out 2025",
                        data_inicio=hoje - timedelta(days=10), data_conclusao=hoje + timedelta(days=50),
                        link_acesso="https://zoom.us/j/222222"),
    Turma.objects.create(treinamento=treinamentos[2], nome="React - Turma Intensiva",
                        data_inicio=hoje, data_conclusao=hoje + timedelta(days=30),
                        link_acesso="https://zoom.us/j/333333"),
]
print(f"{len(turmas)} turmas criadas")

# Criar Recursos
recursos = [
    # Turma 1 (futura)
    Recurso.objects.create(turma=turmas[0], tipo_recurso='pdf', acesso_previo=True, draft=False,
                          nome_recurso='Guia de Instalacao', descricao_recurso='Setup inicial', ordem=1),
    Recurso.objects.create(turma=turmas[0], tipo_recurso='video', acesso_previo=True, draft=False,
                          nome_recurso='Apresentacao', descricao_recurso='Overview', ordem=2),
    Recurso.objects.create(turma=turmas[0], tipo_recurso='pdf', acesso_previo=False, draft=False,
                          nome_recurso='Aula 01', descricao_recurso='Fundamentos', ordem=3),
    Recurso.objects.create(turma=turmas[0], tipo_recurso='video', acesso_previo=False, draft=True,
                          nome_recurso='Aula 02', descricao_recurso='Em preparacao', ordem=4),
    # Turma 2 (ativa)
    Recurso.objects.create(turma=turmas[1], tipo_recurso='pdf', acesso_previo=True, draft=False,
                          nome_recurso='Setup Django', descricao_recurso='Configuracao', ordem=1),
    Recurso.objects.create(turma=turmas[1], tipo_recurso='video', acesso_previo=False, draft=False,
                          nome_recurso='Aula 01 - Models', descricao_recurso='ORM', ordem=2),
    Recurso.objects.create(turma=turmas[1], tipo_recurso='zip', acesso_previo=False, draft=False,
                          nome_recurso='Codigo Fonte', descricao_recurso='Projeto exemplo', ordem=3),
    Recurso.objects.create(turma=turmas[1], tipo_recurso='pdf', acesso_previo=False, draft=True,
                          nome_recurso='Aula 05', descricao_recurso='Avancado', ordem=4),
    # Turma 3 (hoje)
    Recurso.objects.create(turma=turmas[2], tipo_recurso='video', acesso_previo=True, draft=False,
                          nome_recurso='Introducao React', descricao_recurso='Overview', ordem=1),
    Recurso.objects.create(turma=turmas[2], tipo_recurso='pdf', acesso_previo=False, draft=False,
                          nome_recurso='Aula 01 - Componentes', descricao_recurso='React', ordem=2),
]
print(f"{len(recursos)} recursos criados")

# Criar Alunos
alunos_data = [
    {"username": "joao", "nome": "Joao Silva", "email": "joao@email.com", "telefone": "(11) 98765-4321"},
    {"username": "maria", "nome": "Maria Santos", "email": "maria@email.com", "telefone": "(11) 91234-5678"},
    {"username": "pedro", "nome": "Pedro Costa", "email": "pedro@email.com", "telefone": "(11) 99876-5432"},
    {"username": "ana", "nome": "Ana Oliveira", "email": "ana@email.com", "telefone": "(11) 98888-7777"},
]

alunos = []
for data in alunos_data:
    user = User.objects.create_user(username=data["username"], password="senha123", email=data["email"])
    aluno = Aluno.objects.create(user=user, nome=data["nome"], email=data["email"], telefone=data["telefone"])
    alunos.append(aluno)
print(f"{len(alunos)} alunos criados (senha: senha123)")

# Criar Matriculas
matriculas = [
    Matricula.objects.create(turma=turmas[0], aluno=alunos[0]),
    Matricula.objects.create(turma=turmas[1], aluno=alunos[0]),
    Matricula.objects.create(turma=turmas[2], aluno=alunos[0]),
    Matricula.objects.create(turma=turmas[0], aluno=alunos[1]),
    Matricula.objects.create(turma=turmas[1], aluno=alunos[1]),
    Matricula.objects.create(turma=turmas[1], aluno=alunos[2]),
    Matricula.objects.create(turma=turmas[2], aluno=alunos[3]),
]
print(f"{len(matriculas)} matriculas criadas")

print("\n" + "="*50)
print("BANCO POPULADO COM SUCESSO")
print("="*50)
print(f"Treinamentos: {len(treinamentos)}")
print(f"Turmas: {len(turmas)}")
print(f"Recursos: {len(recursos)}")
print(f"Alunos: {len(alunos)}")
print(f"Matriculas: {len(matriculas)}")
print("\nCredenciais:")
print("Admin: admin / admin123")
print("Alunos: joao, maria, pedro, ana / senha123")
print("="*50)