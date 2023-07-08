from django.urls import path
from .views import RelationshipsView, RelationshipsUpdateView

urlpatterns = [
    path("users/friendship/<int:pk>/", RelationshipsView.as_view()),
]
