import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classroom_project.settings')
django.setup()

from django.contrib.auth.models import User
from classroom.models import Treinamento, Turma, Recurso, Aluno, Matricula
from datetime import date, timedelta

print("🚀 Iniciando população do banco de dados...")

# Limpar dados existentes
print("🗑️  Limpando dados antigos...")
Matricula.objects.all().delete()
Recurso.objects.all().delete()
Turma.objects.all().delete()
Treinamento.objects.all().delete()
Aluno.objects.filter(user__is_staff=False).delete()
User.objects.filter(is_staff=False).delete()

# 1. Criar Treinamentos
print("\n📚 Criando treinamentos...")
treinamentos = [
    Treinamento.objects.create(
        nome="Python para Iniciantes",
        descricao="Aprenda Python do zero com projetos práticos"
    ),
    Treinamento.objects.create(
        nome="Django e DRF Avançado",
        descricao="Desenvolvimento de APIs REST com Django Rest Framework"
    ),
    Treinamento.objects.create(
        nome="React Moderno",
        descricao="Construa aplicações web modernas com React e Hooks"
    ),
]
print(f"✅ {len(treinamentos)} treinamentos criados")

# 2. Criar Turmas
print("\n🎓 Criando turmas...")
hoje = date.today()

turmas = [
    Turma.objects.create(
        treinamento=treinamentos[0],
        nome="Python Iniciantes - Turma Janeiro 2026",
        data_inicio=hoje + timedelta(days=60),
        data_conclusao=hoje + timedelta(days=150),
        link_acesso="https://zoom.us/j/111111"
    ),
    Turma.objects.create(
        treinamento=treinamentos[1],
        nome="Django DRF - Turma Outubro 2025",
        data_inicio=hoje - timedelta(days=10),
        data_conclusao=hoje + timedelta(days=50),
        link_acesso="https://zoom.us/j/222222"
    ),
    Turma.objects.create(
        treinamento=treinamentos[2],
        nome="React - Turma Intensiva",
        data_inicio=hoje,
        data_conclusao=hoje + timedelta(days=30),
        link_acesso="https://zoom.us/j/333333"
    ),
]
print(f"✅ {len(turmas)} turmas criadas")

# 3. Criar Recursos
print("\n📁 Criando recursos...")

recursos_turma1 = [
    Recurso.objects.create(
        turma=turmas[0],
        tipo_recurso='pdf',
        acesso_previo=True,
        draft=False,
        nome_recurso='Guia de Instalação do Python',
        descricao_recurso='Material preparatório para configurar seu ambiente',
        url_recurso='https://python.org/downloads',
        ordem=1
    ),
    Recurso.objects.create(
        turma=turmas[0],
        tipo_recurso='video',
        acesso_previo=True,
        draft=False,
        nome_recurso='Apresentação do Curso',
        descricao_recurso='Vídeo de boas-vindas e overview do curso',
        url_recurso='https://youtube.com/watch?v=exemplo1',
        ordem=2
    ),
    Recurso.objects.create(
        turma=turmas[0],
        tipo_recurso='pdf',
        acesso_previo=False,
        draft=False,
        nome_recurso='Aula 01 - Variáveis e Tipos',
        descricao_recurso='Primeira aula sobre fundamentos',
        ordem=3
    ),
    Recurso.objects.create(
        turma=turmas[0],
        tipo_recurso='video',
        acesso_previo=False,
        draft=True,
        nome_recurso='Aula 02 - Estruturas de Controle',
        descricao_recurso='Aula em preparação',
        ordem=4
    ),
]

recursos_turma2 = [
    Recurso.objects.create(
        turma=turmas[1],
        tipo_recurso='pdf',
        acesso_previo=True,
        draft=False,
        nome_recurso='Setup do Projeto Django',
        descricao_recurso='Guia de configuração inicial',
        ordem=1
    ),
    Recurso.objects.create(
        turma=turmas[1],
        tipo_recurso='video',
        acesso_previo=False,
        draft=False,
        nome_recurso='Aula 01 - Models e ORM',
        descricao_recurso='Trabalhando com banco de dados',
        url_recurso='https://youtube.com/watch?v=exemplo2',
        ordem=2
    ),
    Recurso.objects.create(
        turma=turmas[1],
        tipo_recurso='zip',
        acesso_previo=False,
        draft=False,
        nome_recurso='Código Fonte - Projeto Exemplo',
        descricao_recurso='Download do código completo',
        ordem=3
    ),
    Recurso.objects.create(
        turma=turmas[1],
        tipo_recurso='pdf',
        acesso_previo=False,
        draft=True,
        nome_recurso='Aula 05 - Avançado',
        descricao_recurso='Material em preparação',
        ordem=4
    ),
]

recursos_turma3 = [
    Recurso.objects.create(
        turma=turmas[2],
        tipo_recurso='video',
        acesso_previo=True,
        draft=False,
        nome_recurso='Introdução ao React',
        descricao_recurso='Overview e preparação',
        url_recurso='https://youtube.com/watch?v=exemplo3',
        ordem=1
    ),
    Recurso.objects.create(
        turma=turmas[2],
        tipo_recurso='pdf',
        acesso_previo=False,
        draft=False,
        nome_recurso='Aula 01 - Componentes',
        descricao_recurso='Criando componentes React',
        ordem=2
    ),
]

total_recursos = len(recursos_turma1) + len(recursos_turma2) + len(recursos_turma3)
print(f"✅ {total_recursos} recursos criados")

# 4. Criar Alunos
print("\n👨‍🎓 Criando alunos...")
alunos_data = [
    {"username": "joao", "nome": "João Silva", "email": "joao@email.com", "telefone": "(11) 98765-4321"},
    {"username": "maria", "nome": "Maria Santos", "email": "maria@email.com", "telefone": "(11) 91234-5678"},
    {"username": "pedro", "nome": "Pedro Costa", "email": "pedro@email.com", "telefone": "(11) 99876-5432"},
    {"username": "ana", "nome": "Ana Oliveira", "email": "ana@email.com", "telefone": "(11) 98888-7777"},
]

alunos = []
for aluno_data in alunos_data:
    user = User.objects.create_user(
        username=aluno_data["username"],
        password="senha123",
        email=aluno_data["email"]
    )
    
    aluno = Aluno.objects.create(
        user=user,
        nome=aluno_data["nome"],
        email=aluno_data["email"],
        telefone=aluno_data["telefone"]
    )
    alunos.append(aluno)

print(f"✅ {len(alunos)} alunos criados")
print("   Senha padrão: senha123")

# 5. Criar Matrículas
print("\n📝 Criando matrículas...")

matriculas = [
    Matricula.objects.create(turma=turmas[0], aluno=alunos[0]),
    Matricula.objects.create(turma=turmas[1], aluno=alunos[0]),
    Matricula.objects.create(turma=turmas[2], aluno=alunos[0]),
    Matricula.objects.create(turma=turmas[0], aluno=alunos[1]),
    Matricula.objects.create(turma=turmas[1], aluno=alunos[1]),
    Matricula.objects.create(turma=turmas[1], aluno=alunos[2]),
    Matricula.objects.create(turma=turmas[2], aluno=alunos[3]),
]

print(f"✅ {len(matriculas)} matrículas criadas")

print("\n" + "="*60)
print("🎉 BANCO DE DADOS POPULADO COM SUCESSO!")
print("="*60)
print(f"\n📊 Resumo:")
print(f"   • {len(treinamentos)} Treinamentos")
print(f"   • {len(turmas)} Turmas")
print(f"   • {total_recursos} Recursos")
print(f"   • {len(alunos)} Alunos")
print(f"   • {len(matriculas)} Matrículas")
print(f"\n🔑 Credenciais:")
print(f"   Admin: admin / admin123")
print(f"   Alunos: joao, maria, pedro, ana / senha123")
print("="*60)