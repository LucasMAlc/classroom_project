import os
from datetime import date
from django.contrib.auth.models import User
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Treinamento, Turma, Recurso, Aluno, Matricula
from .serializers import (
    TreinamentoSerializer,
    TurmaSerializer,
    RecursoSerializer,
    AlunoSerializer,
    MatriculaSerializer,
    UserRegistrationSerializer,
    TurmaAlunoSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .filters import TurmaFilter, RecursoFilter

class DownloadRecursoView(APIView):
    """Endpoint para download seguro de recursos"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, recurso_id):
        recurso = get_object_or_404(Recurso, id=recurso_id)
        
        # Verificar se o usuário tem permissão
        user = request.user
        
        # Admin pode baixar qualquer recurso
        if user.is_staff:
            if not recurso.arquivo:
                return Response(
                    {'error': 'Recurso não possui arquivo'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            file_path = recurso.arquivo.path
            if os.path.exists(file_path):
                return FileResponse(
                    open(file_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(file_path)
                )
            raise Http404("Arquivo não encontrado")
        
        # Aluno precisa validar permissões
        try:
            aluno = user.aluno
            
            # Verificar se está matriculado na turma
            if not Matricula.objects.filter(
                aluno=aluno,
                turma=recurso.turma,
                ativo=True
            ).exists():
                return Response(
                    {'error': 'Você não está matriculado nesta turma'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Aplicar regras de negócio
            hoje = date.today()
            turma_iniciou = hoje >= recurso.turma.data_inicio
            
            # Verificar se pode acessar
            if recurso.draft:
                return Response(
                    {'error': 'Recurso não disponível'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if not turma_iniciou and not recurso.acesso_previo:
                return Response(
                    {'error': 'Recurso disponível apenas após início da turma'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Permitir download
            if not recurso.arquivo:
                return Response(
                    {'error': 'Recurso não possui arquivo'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            file_path = recurso.arquivo.path
            if os.path.exists(file_path):
                return FileResponse(
                    open(file_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(file_path)
                )
            raise Http404("Arquivo não encontrado")
            
        except Aluno.DoesNotExist:
            return Response(
                {'error': 'Perfil de aluno não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

class IsAdminUser(permissions.BasePermission):
    """Permissão apenas para administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class TreinamentoViewSet(viewsets.ModelViewSet):
    queryset = Treinamento.objects.all()
    serializer_class = TreinamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        """Permite leitura para todos autenticados, escrita só admin"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUser()]


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TurmaFilter

    def get_permissions(self):
        """Permite leitura para todos autenticados, escrita só admin"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        """Admin vê tudo, aluno vê apenas suas turmas"""
        user = self.request.user
        if user.is_staff:
            return Turma.objects.all()
        
        # Retorna turmas do aluno
        try:
            aluno = user.aluno
            return Turma.objects.filter(
                matriculas__aluno=aluno,
                matriculas__ativo=True
            ).distinct()
        except Aluno.DoesNotExist:
            return Turma.objects.none()


class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_class = RecursoFilter 

    def get_queryset(self):
        """Permite filtrar por turma"""
        queryset = Recurso.objects.all()
        turma_id = self.request.query_params.get('turma', None)
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        return queryset


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Admin pode criar/editar, aluno pode ver próprio perfil"""
        if self.action in ['list', 'create', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Admin vê todos, aluno vê apenas ele mesmo"""
        user = self.request.user
        if user.is_staff:
            return Aluno.objects.all()
        return Aluno.objects.filter(user=user)


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Permite filtrar por turma ou aluno"""
        queryset = Matricula.objects.all()
        turma_id = self.request.query_params.get('turma', None)
        aluno_id = self.request.query_params.get('aluno', None)
        
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        
        return queryset


class MeusDadosView(APIView):
    """Endpoint para o aluno ver seus próprios dados"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            aluno = request.user.aluno
            serializer = AlunoSerializer(aluno)
            return Response(serializer.data)
        except Aluno.DoesNotExist:
            return Response(
                {'error': 'Perfil de aluno não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class MinhasTurmasView(APIView):
    """Endpoint para o aluno ver suas turmas com regras de negócio"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            aluno = request.user.aluno
            turmas = Turma.objects.filter(
                matriculas__aluno=aluno,
                matriculas__ativo=True
            ).distinct()
            
            serializer = TurmaAlunoSerializer(turmas, many=True)
            return Response(serializer.data)
        except Aluno.DoesNotExist:
            return Response(
                {'error': 'Perfil de aluno não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class RegistrationView(APIView):
    """Endpoint para registro de novos alunos"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Usuário criado com sucesso'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)