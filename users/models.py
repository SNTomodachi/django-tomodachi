from django.db.models import CharField, EmailField, BooleanField
from django.contrib.auth.models import AbstractUser
from relationships.models import Relationships
from django.db.models import Q
from django.db.models.query import QuerySet


class User(AbstractUser):
    username = CharField(max_length=150, unique=True)
    email = EmailField(unique=True)
    password = CharField(max_length=150, null=True)
    is_super = BooleanField(default=False)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    def get_friends(self) -> QuerySet["User"]:
        sender_friends = Relationships.objects.filter(sender=self, friends=True).values(
            "receiver"
        )
        receiver_friends = Relationships.objects.filter(
            receiver=self, friends=True
        ).values("sender")

        friend_user_ids = sender_friends.union(receiver_friends)
        friends = User.objects.filter(pk__in=friend_user_ids)

        return friends
