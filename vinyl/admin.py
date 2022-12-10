from django.contrib import admin

from .models import Vinyl, Comment, Rating, Favourite

admin.site.register(Vinyl)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Favourite)