from rest_framework.permissions import BasePermission
from users.models import User
from .models import Post


class IsUserIncludedInPostPrivacy(BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        user: User = request.user
        post_user: User = obj.user

        if user == obj.user:
            post_user_friends = post_user.get_friends()
            print(post_user_friends)
            return True

        if obj.share_privacy == "public":
            return True
        elif obj.share_privacy == "only_friends":
            post_user_friends = post_user.get_friends()
            print(post_user_friends)
            return user in post_user_friends
        elif obj.share_privacy == "only_me":
            return user.pk == obj.user
        else:
            return user.pk == obj.user
