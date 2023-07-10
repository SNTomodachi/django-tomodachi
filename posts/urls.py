from django.urls import path
from .views import CreatePostView, PostDetailView

urlpatterns = [
    path("posts/", CreatePostView.as_view()),
    path("posts/<int:pk>", PostDetailView.as_view()),
]
