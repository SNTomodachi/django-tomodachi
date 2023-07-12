from django.db.models import Q
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PostSerializer
from .models import Post
from .permissions import (
    IsUserIncludedInPostPrivacy,
    IsUserIncludedInCommentsPostPrivacy,
)
from comments.serializers import CommentSerializer
from comments.models import Comment
from reactions.serializers import ReactionSerializer
from reactions.models import Reaction
from users.models import User


class CreatePostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(
            share_privacy="only_friends", user__in=User.get_friends(request.user.id)
        ) | Post.objects.filter(share_privacy="public")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserIncludedInPostPrivacy]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        comments_url = f"/api/posts/{instance.id}/comments/"
        reactions_url = f"/api/posts/{instance.id}/reactions/"
        serializer.data["comments_url"] = comments_url
        serializer.data["reactions_url"] = reactions_url

        return Response(serializer.data)


class CommentPostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserIncludedInCommentsPostPrivacy]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)

        serializer.save(post=post, user=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs["pk"]

        return Comment.objects.filter(post_id=post_id)


class ReactionsPostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ReactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserIncludedInPostPrivacy]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)

        serializer.save(post=post, user=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs["pk"]

        return Reaction.objects.filter(post_id=post_id)
