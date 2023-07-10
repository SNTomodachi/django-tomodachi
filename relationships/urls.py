from django.urls import path
from .views import RelationshipsView, RelationshipsUpdateView

urlpatterns = [
    path("users/relationships/<int:pk>/", RelationshipsView.as_view()),
]
