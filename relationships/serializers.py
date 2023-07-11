from rest_framework import serializers
from .models import Relationships


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationships
        fields = [
            "id",
            "sender",
            "receiver",
            "friend",
            "following",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "sender",
            "receiver",
            "friend",
            "following",
            "created_at",
            "updated_at",
        ]

