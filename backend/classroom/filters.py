from django_filters import rest_framework as filters
from .models import Turma, Recurso


class TurmaFilter(filters.FilterSet):
    treinamento = filters.NumberFilter(field_name='treinamento__id')
    treinamento_nome = filters.CharFilter(field_name='treinamento__nome', lookup_expr='icontains')
    data_inicio_after = filters.DateFilter(field_name='data_inicio', lookup_expr='gte')
    data_inicio_before = filters.DateFilter(field_name='data_inicio', lookup_expr='lte')
    
    class Meta:
        model = Turma
        fields = ['treinamento', 'treinamento_nome', 'data_inicio_after', 'data_inicio_before']


class RecursoFilter(filters.FilterSet):
    turma = filters.NumberFilter(field_name='turma__id')
    tipo_recurso = filters.CharFilter(field_name='tipo_recurso')
    acesso_previo = filters.BooleanFilter(field_name='acesso_previo')
    draft = filters.BooleanFilter(field_name='draft')
    
    class Meta:
        model = Recurso
        fields = ['turma', 'tipo_recurso', 'acesso_previo', 'draft']