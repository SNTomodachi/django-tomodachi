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
        if obj:
            return request.user.is_authenticated and obj.receiver == request.user
        else:
            raise ValidationError("This friendship not already exists.")

class IsAccountFollowers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj:
            return request.user.is_authenticated and obj.sender == request.user
        else:
            raise ValidationError("This friendship not already exists.")