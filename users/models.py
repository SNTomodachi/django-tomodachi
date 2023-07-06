from django.db.models import CharField, EmailField, BooleanField, ForeignKey, DO_NOTHING
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = CharField(max_length=150, unique=True)
    email = EmailField(unique=True)
    password = CharField(max_length=150, null=True)
    is_super = BooleanField(default=False)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    #    posts = ForeignKey("posts.Post", on_delete=DO_NOTHING, related_name="user_posts")
