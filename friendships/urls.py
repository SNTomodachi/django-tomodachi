from django.urls import path
from .views import (
    FriendshipView,
    FriendshipRequestView,
    FriendshipRequestDetailView,
)

app_name = "friendships"

urlpatterns = [
    path("users/<int:user_id>/friends/", FriendshipView.as_view()),
    path("users/<int:user_id>/friendship_requests/", FriendshipRequestView.as_view()),
    path(
        "users/<int:user_id>/friendship_requests/<int:id>/",
        FriendshipRequestDetailView.as_view(),
    ),
]
