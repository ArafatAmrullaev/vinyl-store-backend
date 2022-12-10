from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Vinyl(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)
    pic = models.ImageField(upload_to='vinyls')
    extra_pic1 = models.ImageField(upload_to='vinyls', blank=True, null=True)
    extra_pic2 = models.ImageField(upload_to='vinyls', blank=True, null=True)
    extra_pic3 = models.ImageField(upload_to='vinyls', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def average_rating(self):
            ratings = [rating.value for rating in self.ratings.all()]
            if ratings:
                return sum(ratings) / len(ratings)
            return 0


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Favourite(models.Model):
    user = models.ForeignKey(User, related_name='favourites', on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, related_name='favourites', on_delete=models.CASCADE)