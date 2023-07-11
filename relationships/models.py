from django.db import models


class RelationshipStatus(models.TextChoices):
    A = "accepted"
    P = "pending"
    N = "never"
class Relationships(models.Model):
    sender = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="receiver"
    )
    following = models.BooleanField(default=True)
    friend = models.CharField(
        choices=RelationshipStatus.choices, default=RelationshipStatus.N, max_length=25
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
