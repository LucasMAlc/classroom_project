# Classroom Project - Backend

API REST para gestão de turmas.

## Quick Start
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar banco
python manage.py migrate

# Criar admin
python manage.py createsuperuser

# Popular dados de teste
python populate_db.py

# Rodar servidor
python manage.py runserver
```

## Endpoints Principais

**Autenticação:**
- `POST /api/token/` - Login
- `POST /api/registro/` - Criar conta

**Aluno:**
- `GET /api/meus-dados/` - Perfil
- `GET /api/minhas-turmas/` - Turmas matriculadas

**Admin:**
- `/api/treinamentos/`, `/api/turmas/`, `/api/recursos/`, `/api/alunos/`, `/api/matriculas/`

**Documentação:**
- `/api/docs/` - Swagger UI

## Usuários de Teste

- Admin: `admin` / `admin123`
- Alunos: `joao`, `maria`, `pedro`, `ana` / `senha123`

## Testes
```bash
python test_api_completo.py
```

## Tecnologias

Python 3.13 | Django 5.2.7 | DRF 3.16.1 | JWT | SQLite