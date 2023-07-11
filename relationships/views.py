from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from django.shortcuts import get_object_or_404
from .models import Relationships, RelationshipStatus
from .serializers import RelationshipSerializer
from .permissions import IsAccountOwner, IsAccountRetriever, IsAccountFollowers
from users.models import User


class RelationshipsView(ListCreateAPIView):
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

class FriendshipView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Relationships.objects.filter(receiver=user, friend=RelationshipStatus.P)
    
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
        sender = get_object_or_404(User, pk=self.kwargs["pk"])
        receiver = self.request.user
        relationship = get_object_or_404(
            Relationships, sender=sender, receiver=receiver
        )
        relationship.friend = RelationshipStatus.N
        relationship.save()
        return relationship


class FollowersView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountFollowers]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def get_object(self):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user
        relationship = get_object_or_404(
            Relationships, receiver=receiver, sender=sender, following=True
        )
        return relationship

    def perform_create(self, serializer):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user

        relationship = Relationships.objects.filter(sender=sender, receiver=receiver)
        if relationship.exists() and relationship.first().following == True:
            raise ValidationError("This relationship already exists.")
        else:
            if sender.id != receiver.id:
                serializer.save(
                    sender=sender,
                    receiver=receiver,
                    following=True,
                    friend=RelationshipStatus.N,
                )
            else:
                raise ValidationError("Sender and receiver cannot be the same user.")

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        relationships = Relationships.objects.filter(
            Q(receiver=user) | Q(sender=user), following=True
        )
        page = self.paginate_queryset(relationships)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relationships, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user
        relationship = get_object_or_404(
            Relationships, receiver=receiver, sender=sender, following=True
        )
        relationship.following = False

        if relationship.friend == RelationshipStatus.N:
            print(relationship.friend)
            relationship.delete()
        else:
            relationship.save()
        return relationship
