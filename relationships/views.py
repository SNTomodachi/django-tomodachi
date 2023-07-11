from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Relationships, RelationshipStatus
from .serializers import RelationshipSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAccountOwner, IsAccountRetriever
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError


class RelationshipsView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def perform_create(self, serializer):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user

        relationship = Relationships.objects.filter(
            sender=sender, receiver=receiver
        ).first()

        if relationship:
            if relationship.friend in [RelationshipStatus.A, RelationshipStatus.P]:
                raise ValidationError("This relationship already exists.")
        else:
            if sender != receiver:
                serializer.save(
                    sender=sender, receiver=receiver, friend=RelationshipStatus.P
                )
            else:
                raise ValidationError("Sender and receiver cannot be the same user.")

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk")

        if pk is not None and user.pk != pk:
            raise ValidationError("You can't see frienship requests from another user.")
        return Relationships.objects.filter(sender=user)


class RelationshipsUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRetriever]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def get_object(self):
        sender = get_object_or_404(User, pk=self.kwargs["pk"])
        receiver = self.request.user
        relationship = get_object_or_404(
            Relationships, sender=sender, receiver=receiver
        )
        return relationship

    def perform_update(self, serializer):
        sender = get_object_or_404(User, pk=self.kwargs["pk"])
        receiver = self.request.user
        relationship = get_object_or_404(
            Relationships, sender=sender, receiver=receiver
        )

        relationship.friend = RelationshipStatus.A
        relationship.following = True
        relationship.save()
        return relationship

    def perform_destroy(self, instance):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user

        relationship = Relationships.objects.filter(
            sender=sender, receiver=receiver
        ).first()

        return relationship.delete()


class FollowersView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()
    lookup_url_kwarg = "pk"

    def perform_create(self, serializer):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user

        relationship = Relationships.objects.filter(
            sender=sender, receiver=receiver
        ).exists()

        if relationship:
            raise ValidationError("This following already exists.")
        else:
            if sender != receiver:
                serializer.save(
                    sender=sender, receiver=receiver, friend=RelationshipStatus.N
                )
            else:
                raise ValidationError("Sender and receiver cannot be the same user.")

    def list(self, request, *args, **kwargs):
        followers = Relationships.objects.get(sender=self.request.user)
        return followers
