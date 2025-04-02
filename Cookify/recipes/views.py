from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Category, Recipe
from cooks.models import Cook

# Helper functions
def handle_error(request, message:str):
    created_recipe_id = request.session.pop('created_recipe_id', None)
    if created_recipe_id:
        created_recipe = Recipe.objects.get(pk=created_recipe_id)
        created_recipe.delete()
    messages.error(request, message)
    return redirect(request.path)

# Create your views here.
def home(request):
    return render(request, 'recipe/index.html')

@login_required
def add_recipe(request):
    if not request.POST:
        context = {
            'categories': Category.objects.all(),
            'veganity_choices': Recipe.VEGANITY_CHOICES
        }
        return render(request, 'recipe/add_recipe.html', context)
    else:
        title = request.POST.get('title')
        image = request.FILES.get('recipe-image', None)
        categories = request.POST.getlist('categories')
        veganity = request.POST.get('veganity')
        discription = request.POST.get('discription')

        if not (title and image and categories and veganity and discription):
            return handle_error(request, 'Please fill all fields !')

        try:
            veganity = int(veganity)
        except ValueError:
            return handle_error(request, 'Invalid vaganity value !')

        cook = Cook.objects.get_or_create(core_user=request.user)[0]
        recipe = Recipe.objects.create(
            cook=cook,
            title=title,
            image=image,
            veganity_status=veganity,
            discription=discription
        )
        request.session['created_recipe_id'] = recipe.pk
        try:
            recipe.full_clean()
        except ValidationError as err:
            return handle_error(request, err.messages[0])
        recipe.save()
        
        categories = Category.objects.filter(id__in=categories)
        recipe.categories.set(categories)
        next_url = request.POST.get('next', '')
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
            next_url = "../../"
        return redirect(f"../../{next_url}")