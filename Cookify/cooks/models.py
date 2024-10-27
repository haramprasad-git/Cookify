from typing import Iterable
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for the users
class Cook(models.Model):
    DELETE_CHOICES = ((1, 'Live'), (0, 'Removed'))

    name = models.CharField(max_length=200)
    core_user = models.OneToOneField(User, related_name='cook', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_pictures/')
    phone = models.CharField(max_length=15)
    # Social media profiles
    facebook = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    x = models.URLField(max_length=200, blank=True)
    threads = models.URLField(max_length=200, blank=True)

    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=1)
    signed_up_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

# Model for users's personal cookbook
class KitchenBook(models.Model):
    owner = models.OneToOneField(Cook, related_name='kitchen_book', on_delete=models.CASCADE)
    favorite_recipes = models.ManyToManyField('recipes.Recipe', related_name='liked_cooks')
    followed_cooks = models.ManyToManyField(Cook, related_name='followers')

    def __str__(self) -> str:
        return self.owner.__str__()