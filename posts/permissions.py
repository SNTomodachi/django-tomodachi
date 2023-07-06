from rest_framework.permissions import IsAuthenticated, BasePermission
from users.models import User
from .models import Post


class IsFriend(BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        user: User = request.user

        print(user, obj)

        if obj.share_privacy == "public":
            return True
        elif obj.share_privacy == "only_friends":
            return user in obj.user.friends.all()
        elif obj.share_privacy == "only_me":
            return user.pk == obj.user
        else:
            return False
