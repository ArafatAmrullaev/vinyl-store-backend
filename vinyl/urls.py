from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import VinylViewSet, CommentViewSet, FavouriteViewSet, add_rating, add_to_favourite

router = DefaultRouter()
router.register('vinyls', VinylViewSet)
router.register('comments', CommentViewSet)
router.register('favourites', FavouriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vinyls/add_rating/<int:v_id>/', add_rating),
    path('vinyls/add_to_favourite/<int:v_id>/', add_to_favourite),
]