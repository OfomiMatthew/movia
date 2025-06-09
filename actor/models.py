from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Actor(models.Model):
  name = models.CharField(max_length=1000)
  picture = models.ImageField(blank=True)
  slug = models.SlugField(null=True)
  movies = models.ManyToManyField('movia.Movie')
  
  def get_absolute_url(self):
      return reverse('actors',args=[self.slug])
  
  
  def __str__(self):
    return self.name 
  
  def save(self,*args,**kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    return super().save(*args,**kwargs)
      
  
