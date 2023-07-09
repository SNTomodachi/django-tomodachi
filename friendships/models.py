from django.db.models import Model, ForeignKey, CASCADE, BooleanField, DateTimeField


class Friendship(Model):
    class Meta:
        ordering = ["id"]

    sender = ForeignKey("users.User", on_delete=CASCADE, related_name="sender")
    receiver = ForeignKey("users.User", on_delete=CASCADE, related_name="receiver")
    accepted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
