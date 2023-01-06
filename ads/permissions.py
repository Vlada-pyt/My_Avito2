from rest_framework.permissions import BasePermission

from ads.models import UserRoles


class  IsSelectionOwner(BasePermission):
    message = "Вы не имеете доступа"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class IsAdOwnerOrStaff(BasePermission):
    message = "Вы не имеете доступа"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author_id or request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
        return False







