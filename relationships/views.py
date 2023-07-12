from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from django.shortcuts import get_object_or_404 , get_list_or_404
from .models import Relationships, RelationshipStatus
from .serializers import RelationshipSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsAccountOwner,
    IsFriendshipReceiver,
    IsAccountFollowers,
)
from users.models import User


class RelationshipsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def get_queryset(self):
        pk = get_object_or_404(User, pk=self.kwargs["pk"])
        return Relationships.objects.filter(
            Q(sender=pk) | Q(receiver=pk), friend=RelationshipStatus.A
        )

class FriendsRequestsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Relationships.objects.filter(receiver=user, friend=RelationshipStatus.P)

class FriendshipRequestView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]
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


class FriendshipRequestUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFriendshipReceiver]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.friend == RelationshipStatus.A:
            raise ValidationError("This friend request has already been accepted.")
        instance.friend = RelationshipStatus.A
        instance.following = True
        serializer.save()
        return serializer.data


    def perform_destroy(self, instance):
        if instance.friend == RelationshipStatus.N:
            raise ValidationError("You are not friends with this user.")
        instance.friend = RelationshipStatus.N
        instance.save()
        return instance


class FollowingView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountFollowers]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def list(self, request, *args, **kwargs):
        relationship =  get_list_or_404(
            Relationships,sender=self.kwargs["pk"], following=True
        )
        page = self.paginate_queryset(relationship)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relationship, many=True)
        return Response(serializer.data)

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

    def perform_destroy(self, instance):
        if instance.following == False:
             raise ValidationError("You are not following with this user.")
        instance.following = False

        if instance.friend == RelationshipStatus.N:
            instance.delete()
        else:
            instance.save()
        return instance

class followsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountFollowers]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()

    def list(self, request, *args, **kwargs):
        relationship =  get_list_or_404(
            Relationships,receiver=self.kwargs["pk"], following=True
        )
        page = self.paginate_queryset(relationship)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(relationship, many=True)
        return Response(serializer.data)
    