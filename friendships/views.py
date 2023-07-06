from django.shortcuts import render
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Friend
from .serializers import FriendSerializer
from .permissions import IsAccountOwner
from users.models import User


class FriendshipView(ListCreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    def perform_create(self, serializer):
        receiver = get_object_or_404(User, pk=self.kwargs["pk"])
        sender = self.request.user
        serializer.save(sender=sender, receiver=receiver)


class FriendshipUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    lookup_url_kwarg = "pk"
