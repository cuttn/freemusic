from django.db import models

# Create your models here.
class MusicContainer(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    spotifyid = models.CharField(max_length=255)