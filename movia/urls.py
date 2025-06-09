from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('pagination/<str:query>/<int:page_number>/',views.pagination,name='pagination'),
    path('movie/<str:imdb_id>/', views.movieDetails, name='movie_details'),
    path('genre/<slug:genre_slug>/',views.genres, name='genres'),
    
    path('add-to-watch/<imdb_id>/',views.add_movies_to_watch,name='add-to-watch'),
    path('add-watched/<imdb_id>/',views.add_movies_watched,name='add-watched'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('watched/', views.watched_list, name='watched_list'),
    path('rate/<imdb_id>/', views.Rate, name='rate'),
    path('like/<username>/<imdb_id>',views.like,name='review.likes'),
    path('unlike/<username>/<imdb_id>',views.unlike,name='review.unlikes'),
    path('comment/<str:username>/<str:imdb_id>/', views.add_comment, name='add_comment'),
    # path('<str:imdb_id>/comment/', views.add_comment, name='add_comment'),
]
