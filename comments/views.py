from rest_framework.generics import ListCreateAPIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from posts.permissions import IsUserIncludedInCommentsPostPrivacy
from posts.models import Post


class CommentPostView(ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permissions = [IsAuthenticated, IsUserIncludedInCommentsPostPrivacy]

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)

        serializer.save(post=post, user=self.request.user)


class CommentReplyView(ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permissions = [IsAuthenticated, IsUserIncludedInCommentsPostPrivacy]

    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)
        comment_id = self.kwargs["comment_id"]
        parent_comment = Comment.objects.get(id=comment_id)

        serializer.save(parent=parent_comment, post=post, user=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)
        comment_id = self.kwargs["comment_id"]
        comment = Comment.objects.get(id=comment_id)

        return Comment.objects.filter(parent=comment)
