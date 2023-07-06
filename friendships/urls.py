from django.urls import path
from .views import FriendshipView,FriendshipUpdateView

urlpatterns = [
    path("users/<int:pk>/friendship/", FriendshipView.as_view()),
    path("users/<int:pk>/friendship/<int:pk2>/", FriendshipUpdateView.as_view()),
]
