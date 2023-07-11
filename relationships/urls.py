from django.urls import path
from .views import RelationshipsView, RelationshipsUpdateView,FollowersView

urlpatterns = [
    path("users/relationships/<int:pk>/", RelationshipsView.as_view()),
    path("users/friendship/<int:pk>/", RelationshipsUpdateView.as_view()),
    path("users/following/<int:pk>/", FollowersView.as_view()),
    
]
