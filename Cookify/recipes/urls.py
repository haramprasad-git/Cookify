from django.urls import path
from . import views

# URLs for recipe app
urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/all/', views.all_recipes, name='all_recipes'),
    path('recipe/post/<id>/', views.show_recipe_post, name='recipe_post'),
    path('recipe/like/dislike/<target>/', views.like_or_dislike, name='like_or_dislike')
]