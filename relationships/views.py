from django.shortcuts import render
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Relationships
from .serializers import RelationshipsSerializer
from .permissions import IsAccountOwner
from users.models import User


class RelationshipsView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipsSerializer
    queryset = Relationships.objects.all()

    def perform_create(self, serializer):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user
        serializer.save(sender=sender, receiver=receiver, friend=False)

    def delete(self):
        sender = self.request.user
        Relationship = get_object_or_404(User, sender=sender)
        Relationship.delete()


class RelationshipsUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = RelationshipsSerializer
    queryset = Relationships.objects.all()
    lookup_url_kwarg = "pk"
