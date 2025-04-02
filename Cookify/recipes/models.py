import os
from django.db import models
from django.core.validators import MaxValueValidator
from django.dispatch import receiver
from cooks.models import Cook
from cooks.validators import validate_file_size, validate_image_type

# Create your models here.

# Model for recipe catogories
class Category(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField()

    def __str__(self) -> str:
        return self.title

# Model for recipes
class Recipe(models.Model):
    REMOVE_CHOICES = ((1, 'Live'), (0, 'Removed'))
    VEGANITY_CHOICES = ((1, 'Vegetarian'), (2, 'Non-Vegetarian'), (3, 'Egg Only'))

    title = models.CharField(max_length=200)
    discription = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', validators=[validate_file_size, validate_image_type])
    categories = models.ManyToManyField(Category, related_name='products') # eg. Dessert, Breakfast, etc.
    cook = models.ForeignKey(Cook, related_name='posts', on_delete=models.CASCADE) # The cook who posted the recipe
    veganity_status = models.IntegerField(choices=VEGANITY_CHOICES)
    remove_status = models.IntegerField(choices=REMOVE_CHOICES, default=1)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
@receiver(models.signals.post_delete, sender=Recipe)
def delete_image_from_file_system(sender, instance:Recipe, **kwargs):
    if not instance.image:
        return None
    if not os.path.isfile(instance.image.path):
        return None
    os.remove(instance.image.path)

# Model for track comments and rating
class Comment(models.Model):
    commenter = models.ForeignKey(Cook, related_name='comments_posted', on_delete=models.SET_NULL, null=True)
    commented_to = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    discription = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])