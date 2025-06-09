from django.shortcuts import render,get_object_or_404
from .models import Actor
from movia.models import Movie
from django.core.paginator import Paginator

def actors(request,actor_slug):
  actor = get_object_or_404(Actor,slug=actor_slug)
  movies = Movie.objects.filter(actors=actor) 
  paginator = Paginator(movies, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'actor.html', {
        'page_obj': page_obj,
        'actor': actor
    })
  
  



  
