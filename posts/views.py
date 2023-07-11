from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from .models import Post
from .permissions import (
    IsUserIncludedInPostPrivacy,
    IsUserIncludedInCommentsPostPrivacy,
)
from comments.serializers import CommentSerializer
from comments.models import Comment


class CreatePostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated, IsUserIncludedInCommentsPostPrivacy]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)

        serializer.save(post=post, user=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)

        return Comment.objects.filter(post_id=post_id)
