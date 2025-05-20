from django.urls import path
from . import views

# URLs for recipe app
urlpatterns = [
    path('add/', views.add_recipe, name='add_recipe'),
    path('edit/<id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<id>/', views.delete_recipe, name='remove_recipe'),
    path('all/', views.all_recipes, name='all_recipes'),
    path('post/<id>/', views.show_recipe_post, name='recipe_post'),
    path('like/dislike/<target>/', views.like_or_dislike, name='like_or_dislike'),
]