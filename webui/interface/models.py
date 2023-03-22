from django.db import models

# Create your models here.
class SpeechText(models.Model):
    text = models.CharField(max_length=4096)
    
# Create your models here.
class Waypoint(models.Model):
    name = models.CharField(max_length=16)
    x = models.FloatField()
    y = models.FloatField()
    theta = models.FloatField()

