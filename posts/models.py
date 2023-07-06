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

    share_privacy = CharField(choices=SharePrivacy.choices, default="only_friends")
    comments_privacy = CharField(choices=SharePrivacy.choices, default="only_friends")
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)
    media = URLField(null=True)

    # user = ForeignKey("users.User", on_delete=CASCADE, related_name="user_posts")
