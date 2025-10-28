from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    TreinamentoViewSet, TurmaViewSet, RecursoViewSet,
    AlunoViewSet, MatriculaViewSet, MeusDadosView,
    MinhasTurmasView, RegistrationView
)

router = DefaultRouter()
router.register(r'treinamentos', TreinamentoViewSet, basename='treinamento')
router.register(r'turmas', TurmaViewSet, basename='turma')
router.register(r'recursos', RecursoViewSet, basename='recurso')
router.register(r'alunos', AlunoViewSet, basename='aluno')
router.register(r'matriculas', MatriculaViewSet, basename='matricula')

urlpatterns = [
    # Autenticação JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registro/', RegistrationView.as_view(), name='registro'),
    
    # Endpoints específicos do aluno
    path('meus-dados/', MeusDadosView.as_view(), name='meus-dados'),
    path('minhas-turmas/', MinhasTurmasView.as_view(), name='minhas-turmas'),
    
    # Rotas do router
    path('', include(router.urls)),
]