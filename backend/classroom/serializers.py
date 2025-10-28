from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Treinamento, Turma, Recurso, Aluno, Matricula
from datetime import date


class TreinamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treinamento
        fields = ['id', 'nome', 'descricao', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class RecursoSerializer(serializers.ModelSerializer):
    tipo_recurso_display = serializers.CharField(
        source='get_tipo_recurso_display',
        read_only=True
    )
    turma_nome = serializers.CharField(
        source='turma.nome',
        read_only=True
    )

    class Meta:
        model = Recurso
        fields = [
            'id', 'turma', 'turma_nome', 'tipo_recurso',
            'tipo_recurso_display', 'acesso_previo', 'draft',
            'nome_recurso', 'descricao_recurso', 'arquivo',
            'url_recurso', 'ordem', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']


class RecursoAlunoSerializer(serializers.ModelSerializer):
    """Serializer para visualização do aluno (sem campos sensíveis)"""
    tipo_recurso_display = serializers.CharField(
        source='get_tipo_recurso_display',
        read_only=True
    )

    class Meta:
        model = Recurso
        fields = [
            'id', 'tipo_recurso', 'tipo_recurso_display',
            'nome_recurso', 'descricao_recurso', 'arquivo',
            'url_recurso', 'ordem'
        ]


class TurmaSerializer(serializers.ModelSerializer):
    treinamento_nome = serializers.CharField(
        source='treinamento.nome',
        read_only=True
    )
    recursos = RecursoSerializer(many=True, read_only=True)
    total_alunos = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = [
            'id', 'treinamento', 'treinamento_nome', 'nome',
            'data_inicio', 'data_conclusao', 'link_acesso',
            'recursos', 'total_alunos', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def get_total_alunos(self, obj):
        return obj.matriculas.filter(ativo=True).count()


class TurmaAlunoSerializer(serializers.ModelSerializer):
    """Serializer para visualização do aluno com regras de negócio"""
    treinamento = TreinamentoSerializer(read_only=True)
    recursos = serializers.SerializerMethodField()
    pode_acessar = serializers.SerializerMethodField()

    class Meta:
        model = Turma
        fields = [
            'id', 'treinamento', 'nome', 'data_inicio',
            'data_conclusao', 'link_acesso', 'recursos',
            'pode_acessar'
        ]

    def get_pode_acessar(self, obj):
        """Verifica se a turma já iniciou"""
        return date.today() >= obj.data_inicio

    def get_recursos(self, obj):
        """Aplica regras de negócio para recursos"""
        hoje = date.today()
        turma_iniciou = hoje >= obj.data_inicio

        # Regra 2: Antes do início, só recursos com acesso prévio
        if not turma_iniciou:
            recursos = obj.recursos.filter(acesso_previo=True, draft=False)
        # Regra 3: Após início, recursos não draft
        else:
            recursos = obj.recursos.filter(draft=False)

        return RecursoAlunoSerializer(recursos, many=True).data


class AlunoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Aluno
        fields = [
            'id', 'username', 'nome', 'email', 'telefone',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']


class MatriculaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    treinamento_nome = serializers.CharField(
        source='turma.treinamento.nome',
        read_only=True
    )

    class Meta:
        model = Matricula
        fields = [
            'id', 'turma', 'turma_nome', 'treinamento_nome',
            'aluno', 'aluno_nome', 'data_matricula', 'ativo'
        ]
        read_only_fields = ['data_matricula']

    def validate(self, data):
        """Valida se o aluno já está matriculado na turma"""
        turma = data.get('turma')
        aluno = data.get('aluno')
        
        if Matricula.objects.filter(turma=turma, aluno=aluno).exists():
            raise serializers.ValidationError(
                "Aluno já está matriculado nesta turma."
            )
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    nome = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    telefone = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'nome', 'email', 'telefone']

    def create(self, validated_data):
        nome = validated_data.pop('nome')
        email = validated_data.pop('email')
        telefone = validated_data.pop('telefone', '')

        # Cria o User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email
        )

        # Cria o Aluno vinculado
        Aluno.objects.create(
            user=user,
            nome=nome,
            email=email,
            telefone=telefone
        )

        return user