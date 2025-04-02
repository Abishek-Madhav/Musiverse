from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    song_name=models.CharField(max_length=500)
    song_url = models.CharField(max_length=10000)
    song_lyrics = models.TextField(default="No lyrics available")
    image_url = models.CharField(max_length=500)
