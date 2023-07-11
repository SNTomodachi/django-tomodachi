from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Relationships
from users.models import User


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationships
        fields = ["id", "sender","receiver","friend","following", "created_at", "updated_at"]
        read_only_fields = ["id", "sender","receiver","friend","following", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
