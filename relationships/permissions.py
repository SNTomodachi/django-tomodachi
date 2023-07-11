from rest_framework import permissions
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from .models import Relationships
from users.models import User
class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj == request.user
    
class IsAccountRetriever(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        receiver = get_object_or_404(User, pk=view.kwargs["pk"])
        sender = request.user

        relationship = Relationships.objects.filter(
            sender=sender, receiver=receiver
        ).first()

        print(obj)
        if relationship:
            raise ValidationError("This friendship not already exists.")
        else:
            return request.user.is_authenticated 