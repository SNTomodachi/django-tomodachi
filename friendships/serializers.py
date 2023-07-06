from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Friend
from users.models import User


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["id", "status", "sender","receiver", "created_at", "updated_at"]
        read_only_fields = ["id", "status", "sender","receiver", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
