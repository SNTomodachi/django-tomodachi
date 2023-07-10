from rest_framework.generics import (
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Relationships
from .serializers import RelationshipsSerializer
from .permissions import IsAccountOwner
from users.models import User
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.db.models import Q


class RelationshipsView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipsSerializer
    queryset = Relationships.objects.all()

    def perform_create(self, serializer):
        receiver_id = self.kwargs["user_id"]
        sender = self.request.user
        receiver = get_object_or_404(User, pk=receiver_id)

        if sender != receiver:
            serializer.save(sender=sender, receiver=receiver, accepted=False)
        else:
            raise ValidationError("Sender and receiver cannot be the same user.")

    def get_queryset(self):
        user = self.request.user

        if user.pk != self.kwargs["user_id"]:
            raise ValidationError("You can't see frienship requests from another user.")
        return Friendship.objects.filter(receiver=user)


class RelationshipsUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipsSerializer
    queryset = Relationships.objects.all()
    lookup_url_kwarg = "pk"
