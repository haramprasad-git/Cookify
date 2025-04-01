import os
from typing import Iterable
from PIL import Image
from django.dispatch import receiver
from django.db import models
# from django.core.validators import validate_image_file_extension
from django.contrib.auth.models import User
from .validators import validate_file_size, validate_image_type

# Create your models here.

# Model for the users
class Cook(models.Model):
    DELETE_CHOICES = ((1, 'Live'), (0, 'Removed'))

    name = models.CharField(max_length=200)
    core_user = models.OneToOneField(User, related_name='cook', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,
                                        validators=[validate_image_type, validate_file_size])
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

@receiver(models.signals.post_delete, sender=Cook)
def delete_image_from_file_system(sender, instance:Cook, **kwargs):
    if not instance.profile_picture:
        return None
    if not os.path.isfile(instance.profile_picture.path):
        return None
    os.remove(instance.profile_picture.path)

# Model for users's personal cookbook
class KitchenBook(models.Model):
    owner = models.OneToOneField(Cook, related_name='kitchen_book', on_delete=models.CASCADE)
    favorite_recipes = models.ManyToManyField('recipes.Recipe', related_name='liked_cooks', )
    followed_cooks = models.ManyToManyField(Cook, related_name='followers')

    def __str__(self) -> str:
        return self.owner.__str__()