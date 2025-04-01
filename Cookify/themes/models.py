from django.db import models

# Create your models here.

# Model to track settings of the website
class WebSetting(models.Model):
    banner = models.ImageField(upload_to='logos/')
    fevicon = models.ImageField(upload_to='logos/')
    tagline = models.TextField(max_length=200)