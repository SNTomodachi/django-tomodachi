from django.db.models import (
    TextChoices,
    Model,
    CharField,
    TextField,
    DateTimeField,
    URLField,
    ForeignKey,
    CASCADE,
)


class SharePrivacy(TextChoices):
    public = "public"
    only_friends = "only_friends"
    ony_me = "only_me"


class Post(Model):
    class Meta:
        ordering = ["id"]

    text = TextField()
    media = URLField(null=True)
    share_privacy = CharField(
        choices=SharePrivacy.choices, default="only_friends", max_length=12
    )
    comments_privacy = CharField(
        choices=SharePrivacy.choices, default="only_friends", max_length=12
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    user = ForeignKey("users.User", on_delete=CASCADE, related_name="user_posts")
