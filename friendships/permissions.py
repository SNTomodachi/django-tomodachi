from rest_framework import permissions
from users.models import User


class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id")

        return request.user.id == user_id
