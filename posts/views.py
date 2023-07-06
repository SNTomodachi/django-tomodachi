from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView
from .serializers import PostSerializer
from .models import Post


class PostView(ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.all()
