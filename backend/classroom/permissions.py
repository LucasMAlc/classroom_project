from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada: apenas admins podem criar/editar/deletar.
    Usuários autenticados podem apenas ler.
    """
    def has_permission(self, request, view):
        # Permite leitura para usuários autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Escrita apenas para admins
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão customizada: usuários podem ver/editar apenas seus próprios dados,
    admins podem ver/editar tudo.
    """
    def has_object_permission(self, request, view, obj):
        # Admins têm acesso total
        if request.user.is_staff:
            return True
        
        # Verifica se o objeto pertence ao usuário
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False