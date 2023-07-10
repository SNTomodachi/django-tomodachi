from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Relationships
from .serializers import RelationshipSerializer
from .permissions import IsAccountOwner
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
        ).exists()

        if relationship["friend"] :
            raise ValidationError("This relationship already exists.")
        else:
            if sender != receiver:
                serializer.save(sender=sender, receiver=receiver, friend="pending" )
            else:
                raise ValidationError("Sender and receiver cannot be the same user.")

    def get_queryset(self):
        user = self.request.user
        if user.pk != self.kwargs["pk"]:
            raise ValidationError("You can't see frienship requests from another user.")
        return Relationships.objects.filter(sender=user)


class RelationshipsUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipSerializer
    queryset = Relationships.objects.all()
    lookup_url_kwarg = "pk"


    def retrieve(self, request, *args, **kwargs):
        ...

        
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
                serializer.save(sender=sender, receiver=receiver, friend="never")
            else:
                raise ValidationError("Sender and receiver cannot be the same user.")

