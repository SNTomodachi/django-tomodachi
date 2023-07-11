from rest_framework.serializers import ModelSerializer
from .models import Reaction


class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = [
            "id",
            "type",
            "created_at",
            "updated_at",
            "post_id",
            "user_id"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "post_id", "user_id"]
