from rest_framework.permissions import BasePermission
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied


class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj == request.user


class IsFriendshipReceiver(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj:
            return request.user.is_authenticated and obj.receiver == request.user
        else:
            raise PermissionDenied("This friend request does not exist.", code=404)


class IsAccountFollowers(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj:
            return request.user.is_authenticated and obj.sender == request.user
        else:
            raise ValidationError("You not follower this user.")
