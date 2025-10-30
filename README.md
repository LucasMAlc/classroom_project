# Classroom Project

Sistema de gestão de turmas.

## Tecnologias

**Backend:** Python 3.13 | Django 5.2.7 | DRF | JWT | SQLite  
**Frontend:** React 18 | React Router | Axios

## Instalação

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python populate_db.py # Opicional
python manage.py runserver
```

Disponivel em: http://127.0.0.1:8000

### Frontend
```bash
cd frontend
npm install
npm start
```

Disponivel em: http://localhost:3000

## Usuários de Teste

**Admin:** admin / admin123  
**Alunos:** joao, maria, pedro, ana / senha123 (populate_db.py)

## Funcionalidades

### Admin
- CRUD completo de treinamentos, turmas e recursos
- Gerenciar matriculas
- Visualizar todos os dados

### Aluno
- Visualizar turmas matriculadas
- Acessar recursos
- Baixar materiais

## Swagger

- `/api/docs/` -

## Teste
```bash
cd backend
python test_api_completo.py
```

## Estrutura
```
classroom_project/
|-- backend/      # Django + DRF
|-- frontend/     # React
|-- README.md
```
