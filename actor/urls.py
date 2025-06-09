from django.urls import path 
from . import views

urlpatterns = [
  path('actor/<slug:actor_slug>/',views.actors, name='actors'),
]
