from django.urls import path
from . import views

# URLs for recipe app
urlpatterns = [
    path('', views.home, name='home'),
    path('add/recipe/', views.add_recipe, name='add_recipe'),
]