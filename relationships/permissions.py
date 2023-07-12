from rest_framework import permissions
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj == request.user


class IsFriendshipReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj:
            if request.method == "PATCH":
                return request.user.is_authenticated and obj.receiver == request.user
            elif request.method == "DELETE":
                return request.user.is_authenticated and (obj.receiver == request.user or obj.sender == request.user)
        else:
            raise PermissionDenied("This friend request does not exist.", code=404)



class IsAccountFollowers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if obj:
                return request.user.is_authenticated and obj.sender == request.user
            else:
                raise ValidationError("You not follower this user.")
