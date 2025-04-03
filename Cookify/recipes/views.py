from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count, Avg, Func
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
    # 4 most liked recipes in the carousel
    carousel_recipes = list(Recipe.objects.annotate(like_count=Count('liked_cooks'))
                        .order_by('-like_count')
                        .only('id', 'title', 'image')[:4])
    
    # 8 most rated recipies (avoiding unrated ones)
    best_recipes = list(Recipe.objects.annotate(avg_rating=Func(Avg('comments__rating'), function="ROUND"))
                    .exclude(avg_rating__isnull=True)
                    .order_by('avg_rating')[:8])
    
    # 9 more recipies that are not in best recipes or carousel recipes
    excluding_id = {recipe.id for recipe in best_recipes+carousel_recipes}
    more_recipes = list(Recipe.objects.exclude(id__in=excluding_id)
                        .only('id', 'title', 'image', 'posted_at', 'comments')[:9])
    
    # 9 most followed cooks
    famous_cooks = list(Cook.objects.annotate(followers_count=Count('followers'))
                        .order_by('-followers_count')[:9]
                        .only('id', 'name', 'profile_picture', 'followers')[:9])

    context = {
        'carousel_recipes': carousel_recipes,
        'top_category': best_recipes[:2],
        'best_recipes': best_recipes[2:],
        'more_recipes': more_recipes,
        'famous_cooks': famous_cooks
    }
    print(context)
    return render(request, 'recipe/index.html', context)

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
            return handle_error(request, 'Invalid veganity value !')

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
    
def show_recipe(request):
    return render(request, 'recipe/recipe-post.html')