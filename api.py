from django.shortcuts import render
import requests 

# Create your views here.
def index(request):
  query = requests.GET.get('q')
  if query:
    url = "http://www.omdbapi.com/?apikey=89553bad&s" + query
    res = requests.get(url)
    if res.status_code == 200:
      print(res.json())
    else:
      print(res.reason)
      

