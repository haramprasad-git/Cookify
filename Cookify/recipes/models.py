from django.db import models
from django.core.validators import MaxValueValidator
from cooks.models import Cook

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
    image = models.ImageField(upload_to='recipe_images/')
    categories = models.ManyToManyField(Category, related_name='products') # eg. Dessert, Breakfast, etc.
    cook = models.ForeignKey(Cook, related_name='posts', on_delete=models.CASCADE) # The cook who posted the recipe
    veganity_status = models.IntegerField(choices=VEGANITY_CHOICES)
    remove_status = models.IntegerField(choices=REMOVE_CHOICES, default=1)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
# Model for track comments and rating
class Comment:
    commenter = models.ForeignKey(Cook, related_name='comments_posted', on_delete=models.SET_NULL, null=True)
    commented_to = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    discription = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])