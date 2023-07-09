from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "text",
            "media",
            "share_privacy",
            "comments_privacy",
            "created_at",
            "updated_at",
            "user_id",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user_id"]
