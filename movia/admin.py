from django.contrib import admin
from .models import Movie, Genre, Rating, Review, Likes


# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Likes)


