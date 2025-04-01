from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request, 'recipe/index.html')

def add_recipe(request):
    return render(request, 'recipe/add_recipe.html')