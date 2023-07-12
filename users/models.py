from django.db.models import CharField, EmailField, BooleanField
from django.contrib.auth.models import AbstractUser
from relationships.models import Relationships
from django.db.models import Q
from django.db.models.query import QuerySet


class User(AbstractUser):
    username = CharField(max_length=150, unique=True)
    email = EmailField(unique=True)
    password = CharField(max_length=150)
    is_super = BooleanField(default=False)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    def get_friends(self) -> QuerySet["User"]:
        sender_friend_user_ids = Relationships.objects.filter(
            sender=self, friend="accepted"
        ).values_list("receiver_id", flat=True)

        receiver_friend_user_ids = Relationships.objects.filter(
            receiver=self, friend="accepted"
        ).values_list("sender_id", flat=True)

        friend_user_ids = set(sender_friend_user_ids) | set(receiver_friend_user_ids)

        friends = User.objects.filter(id__in=friend_user_ids)

        return friends
