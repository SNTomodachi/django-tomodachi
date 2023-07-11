from django.db.models import Model, CharField, ForeignKey, CASCADE, DateTimeField
from posts.models import Post
from users.models import User


class Comment(Model):
    class Meta:
        ordering = ["id"]

    message = CharField(max_length=300)
    post = ForeignKey(Post, on_delete=CASCADE, related_name="post_comments")
    user = ForeignKey(User, on_delete=CASCADE, related_name="user_comments")
    parent = ForeignKey(
        "self", on_delete=CASCADE, null=True, blank=True, related_name="comment_replies"
    )
    created_at = DateTimeField(auto_now_add=True)
