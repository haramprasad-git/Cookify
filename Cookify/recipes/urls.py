from django.urls import path
from . import views

# URLs for recipe app
urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/add', views.add_recipe, name='add_recipe'),
    path('recipe/post', views.show_recipe, name='recipe_post'),
]