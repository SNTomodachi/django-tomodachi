from django.urls import path
from .views import (
    RelationshipsView,
    FriendsRequestsView,
    FriendshipRequestView,
    FriendshipRequestUpdateDestroyView,
    FollowingView,
)

urlpatterns = [
    path("users/<int:pk>/relationships/", RelationshipsView.as_view()),
    path("friend_requests/", FriendsRequestsView.as_view()),
    path("users/<int:pk>/friend_requests/", FriendshipRequestView.as_view()),
    path("friend_request/<int:pk>/", FriendshipRequestUpdateDestroyView.as_view()),
    path("following/<int:pk>/", FollowingView.as_view()),
]
