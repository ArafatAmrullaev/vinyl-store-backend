from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, action
from rest_framework import filters, mixins
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Vinyl, Comment, Rating, Favourite
from .serializers import VinylSerializer, CommentSerializer, FavouriteSerializer
from .permissions import IsAdminOrReadOnly, IsAuthor


class VinylViewSet(ModelViewSet):
    queryset = Vinyl.objects.all()
    serializer_class = VinylSerializer
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['POST'])
def add_rating(request, v_id):
    user = request.user
    vinyl = get_object_or_404(Vinyl, id=v_id)
    value = request.POST.get('value')

    if not user.is_authenticated:
        raise ValueError('authentication credentials are not provided')

    if not value:
        raise ValueError('value is required')

    if Rating.objects.filter(user=user, vinyl=vinyl).exists():
        rating = Rating.objects.get(user=user, vinyl=vinyl)
        rating.value = value
        rating.save()

    else:
        Rating.objects.create(user=user, vinyl=vinyl, value=value)

    return Response('rating created', 201)


@api_view(['POST'])
def add_to_favourite(request, v_id):
    user = request.user
    vinyl = get_object_or_404(Vinyl, id=v_id)

    if not user.is_authenticated:
        raise ValueError('authentication credentials are not provided')

    if Favourite.objects.filter(user=user, vinyl=vinyl).exists():
        Favourite.objects.filter(user=user, vinyl=vinyl).delete()
    else:
        Favourite.objects.create(user=user, vinyl=vinyl)

    return Response('Added to Favourite', 200)

class FavouriteViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset