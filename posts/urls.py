from django.urls import path
from .views import CreatePostView, PostDetailView, CommentPostView, ReactionsPostView

urlpatterns = [
    path("posts/", CreatePostView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("posts/<int:pk>/comments/", CommentPostView.as_view()),
    path("posts/<int:pk>/reactions/", ReactionsPostView.as_view())
]
