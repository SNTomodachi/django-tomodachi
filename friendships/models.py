from django.db import models

class FriendshipStatus(models.TextChoices):
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"

class Friend(models.Model):
    sender = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="sender")
    receiver= models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="receiver")
    status = models.CharField(max_length=20, choices=FriendshipStatus.choices, default=FriendshipStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
