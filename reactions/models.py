from django.db.models import (
    Model,
    TextChoices,
    CharField,
    DateTimeField,
    ForeignKey,
    CASCADE,
)


class ReactionType(TextChoices):
    like = "like"
    love = "love"
    laught = "laught"
    sad = "sad"
    angry = "angry"


class Reaction(Model):
    class meta:
        ordering = ["id"]

    type =  CharField(choices=ReactionType.choices, default="like", max_length=8)
    created_at = DateTimeField(auto_now_add=True)       
    updated_at = DateTimeField(auto_now=True)

    post = ForeignKey("posts.Post", on_delete=CASCADE, related_name="post_reactions")
    user = ForeignKey("users.User", on_delete=CASCADE, related_name="user_reactions")
