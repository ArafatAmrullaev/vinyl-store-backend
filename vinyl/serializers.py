from rest_framework import serializers

from .models import Vinyl, Rating, Comment, Favourite

class VinylSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinyl
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['added_to_favourite'] = False
        request = self.context.get('request')
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['rating'] = instance.average_rating
        rep['user_rating'] = 0
        if request.user.is_authenticated:
            rep['added_to_favourite'] = Favourite.objects.filter(user=request.user, vinyl= instance).exists()

            if Rating.objects.filter(user=request.user, vinyl=instance).exists():
                rating = Rating.objects.get(user=request.user, vinyl=instance)
                rep['user_rating'] = rating.value
        return rep


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        return rep


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'