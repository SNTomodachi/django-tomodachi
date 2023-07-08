from django.db import models


class Relationships(models.Model):
    sender = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="receiver"
    )
    friend = models.BooleanField(default=False)
    following = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
