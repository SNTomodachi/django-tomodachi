from rest_framework.serializers import ModelSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "message", "post_id", "user_id", "parent_id", "created_at"]
        read_only_fields = ["id", "user_id", "post_id", "parent_id", "created_at"]
