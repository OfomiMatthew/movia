from django.db import models
from django.contrib.auth.models import User 
from movia.models import Movie
from django.db.models.signals import post_save 
from PIL import Image 
from django.conf import settings 
import os 

def user_directory_path(instance,filename):
  profile_pic_name = f'user_{instance.user.id}/profile.jpg'
  full_path = os.path.join(settings.MEDIA_ROOT,profile_pic_name)
  
  if os.path.exists(full_path):
    os.remove(full_path)
  return profile_pic_name 


class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
  first_name = models.CharField(max_length=100,null=True,blank=True)
  last_name = models.CharField(max_length=100,null=True,blank=True)
  location = models.CharField(max_length=100,null=True,blank=True)
  social_url = models.URLField(blank=True,null=True)
  profile_info = models.TextField(blank=True,null=True)
  created = models.DateField(auto_now_add=True)
  to_watch = models.ManyToManyField(Movie,related_name='towatch')
  watched = models.ManyToManyField(Movie,related_name='watched')
  picture = models.ImageField(upload_to=user_directory_path,blank=True,null=True)
  
  
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    SIZE = 250, 250

    if self.picture:
        pic = Image.open(self.picture.path)
        pic.thumbnail(SIZE, Image.LANCZOS)

        # Convert if the image is not in RGB mode (e.g., P or RGBA)
        if pic.mode != 'RGB':
            pic = pic.convert('RGB')

        pic.save(self.picture.path, format='JPEG')
  
  
  # def save(self,*args,**kwargs):
  #   super().save(*args,**kwargs)
  #   SIZE =250,250 
    
  #   if self.picture:
  #     pic = Image.open(self.picture.path)
  #     pic.thumbnail(SIZE,Image.LANCZOS)
  #     pic.save(self.picture.path)
      
      
  def __str__(self):
    return self.user.username 
  
def create_user_profile(sender,instance,created,**kwargs):
  if created:
    Profile.objects.create(user=instance)
    
def save_user_profile(sender,instance,**kwargs):
  instance.profile.save()
  
post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)
