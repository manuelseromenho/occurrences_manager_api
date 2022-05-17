from django.urls import path, include
from rest_framework.routers import DefaultRouter

from occurrences import views
from occurrences.views import OccurrenceViewSet, AuthorViewSet, CreateAuthorView

#using routers
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'occurrences', OccurrenceViewSet)
router.register(r'authors', AuthorViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('pizzas/<int:id>/', views.PizzaView.as_view()),
    path('pizzas/', views.PizzaView.as_view()),
    path('create_author/', CreateAuthorView.as_view(), name="create-author"),
    path('', include(router.urls)),
]

