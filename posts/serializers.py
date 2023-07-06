from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "share_privacy",
            "comments_privacy",
            "text",
            "created_at",
            "media",
        ]
        read_only_fields = ["id", "created_at"]
