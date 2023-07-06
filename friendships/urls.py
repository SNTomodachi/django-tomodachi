from django.urls import path
from .views import FriendshipView,FriendshipUpdateView

urlpatterns = [
    path("users/relationship/<int:pk>/", FriendshipView.as_view()),
]
