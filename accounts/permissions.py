from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Faqat role='admin' bo'lgan foydalanuvchilarga to'liq CRUD ruxsati beradi.
    Boshqa autentifikatsiyadan o'tgan foydalanuvchilarga (masalan seller)
    faqat o'qish (GET) ruxsati beriladi.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, 'role', None) == 'admin' or request.user.is_superuser