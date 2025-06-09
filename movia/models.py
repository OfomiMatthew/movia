from django.db import models
from django.utils.text import slugify
from actor.models import Actor
import requests
from io import BytesIO
from django.core import files
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(null=True)
  
  def get_absolute_url(self):
      return reverse('genres',args=[self.slug])
  
  
  def __str__(self):
    return self.title 
  
  def save(self,*args,**kwargs):
    if not self.slug:
      self.title.replace(" ","-")
      self.slug = slugify(self.title)
    return super().save(*args,**kwargs)
  
  
class Rating(models.Model):
  source = models.CharField(max_length=100)
  rating = models.CharField(max_length=10)
  
  def __str__(self):
    return self.source
  
class Movie(models.Model):
  title = models.CharField(max_length=300)
  year = models.CharField(max_length=100,blank=True,null=True)
  rated = models.CharField(max_length=100,blank=True)
  released = models.CharField(max_length=100,blank=True)
  runtime = models.CharField(max_length=100,blank=True)
  genre = models.ManyToManyField(Genre,blank=True)
  director = models.CharField(max_length=100,blank=True)
  writer = models.CharField(max_length=100,blank=True)
  actors = models.ManyToManyField(Actor,blank=True)
  plot = models.CharField(max_length=1000,blank=True)
  language = models.CharField(max_length=100,blank=True)
  country = models.CharField(max_length=100,blank=True)
  awards = models.CharField(max_length=100,blank=True)
  poster = models.ImageField(upload_to='movies',blank=True)
  poster_url = models.URLField(blank=True)
  ratings = models.ManyToManyField(Rating,blank=True)
  metascore = models.CharField(max_length=100,blank=True)
  imdbRating = models.CharField(max_length=100,blank=True)
  imdbVotes = models.CharField(max_length=100,blank=True)
  imdbID = models.CharField(max_length=100,blank=True)
  type = models.CharField(max_length=100,blank=True)
  dvd = models.CharField(max_length=100,blank=True)
  boxOffice = models.CharField(max_length=100,blank=True)
  production = models.CharField(max_length=100,blank=True)
  website = models.CharField(max_length=100,blank=True)
  totalSeasons = models.CharField(max_length=100,blank=True,null=True)
  
  def __str__(self):
    return self.title
  
  def save(self,*args,**kwargs):
    if self.poster == '' and self.poster_url != '':
      resp = requests.get(self.poster_url)
      pb = BytesIO()
      pb.write(resp.content)
      pb.flush()
      file_name = self.poster_url.split('/')[-1]
      self.poster.save(file_name, files.File(pb), save=False)
    return super().save(*args,**kwargs)
  
  

RATE_CHOICES = [
    (1, 'Terrible'),
    (2, 'Bad'),
    (3, 'Poor'),
    (4, 'Mediocre'),
    (5, 'Watchable'),
    (6, 'Average'),
    (7, 'Good'),
    (8, 'Very Good'),
    (9, 'Excellent'),
    (10, 'Masterpiece'),
]
class Review(models.Model):
 
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  text = models.TextField(max_length=3000,blank=True)
  rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
  likes = models.PositiveIntegerField(default=0)
  unlikes = models.PositiveIntegerField(default=0)
  
  
  @property
  def likers(self):
    return User.objects.filter(likes__review=self, likes__type_like=2)
    
  @property
  def unlikers(self):
    return User.objects.filter(likes__review=self, likes__type_like=1)
  
  def __str__(self):
    return f'{self.user.username} rating for {self.movie} is ({self.rate}/{len(RATE_CHOICES)})'
  
  
class Likes(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_like')
  type_like = models.PositiveSmallIntegerField()
  review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='review_like')
  
  
class Comment(models.Model):
  review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='comments')
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  body = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  
      
  
  
  
