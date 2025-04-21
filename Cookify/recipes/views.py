from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.templatetags.static import static
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count, Avg, Value
from django.db.models.functions import Round, Coalesce
from django.db import OperationalError
from .models import Category, Recipe, Comment
from cooks.models import Cook

# Helper functions
def handle_error(request, message:str, fragment=""):
    created_recipe_id = request.session.pop('created_recipe_id', None)
    if created_recipe_id:
        created_recipe = Recipe.objects.get(pk=created_recipe_id)
        created_recipe.delete()
    messages.error(request, message)
    return redirect(f"{request.path}#{fragment}")

# Create your views here.
def home(request):
    # 4 most liked recipes in the carousel
    carousel_recipes = list(Recipe.objects.annotate(like_count=Count('liked_cooks'))
                        .order_by('-like_count')
                        .only('id', 'title', 'image')[:4])
    
    # 8 most rated recipies
    best_recipes = list(Recipe.objects.annotate(avg_rating=Coalesce(Round(Avg('comments__rating')), Value(0.0)))
                    .order_by('-avg_rating')[:8])
    
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

        try:
            recipe = Recipe.objects.create(
                cook=request.user.cook,
                title=title,
                image=image,
                veganity_status=veganity,
                discription=discription
            )
            request.session['created_recipe_id'] = recipe.pk
            recipe.full_clean()
        except ValidationError as err:
            return handle_error(request, err.messages[0])
        except OperationalError:
            return handle_error(request, 'Sorry, Failed to add recipe !')
        except Exception:
            return handle_error(request, 'Sorry, Unexpected error occured')
        recipe.save()

        categories = Category.objects.filter(id__in=categories)
        recipe.categories.set(categories)
        next_url = request.POST.get('next', '')
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
            next_url = "../../"
        return redirect(f"../../{next_url}")

def all_recipes(request):
    selected_category = int(request.GET.get('cat', '0'))
    selected_vaganity = int(request.GET.get('veg', '0'))
    selected_cook = int(request.GET.get('cook', '0'))
    search_query = request.GET.get('search')

    recipes = Recipe.objects.all()

    if selected_cook != 0:
        print("Cook Selected")
        recipes = recipes.filter(cook__id=selected_cook)
    if selected_category != 0:
        print("Category selected")
        recipes = recipes.filter(categories__id=selected_category)
    if selected_vaganity != 0:
        print("Veganity selected")
        recipes = recipes.filter(veganity_status=selected_vaganity)
    if search_query:
        print("Query")
        recipes = recipes.filter(title__icontains=search_query)

    context = {
        'breadcrumb_bg': static('img/bg-img/breadcumb3.jpg'),
        'categories': Category.objects.only('id', 'title'),
        'veganity_choices': Recipe.VEGANITY_CHOICES,
        'recipes': recipes.annotate(avg_rating=Coalesce(Round(Avg('comments__rating')), Value(0.0)))
    }
    return render(request, 'recipe/recipes.html', context)
    
def show_recipe_post(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.POST:
        # Code for posting comments
        if not request.user.is_authenticated:
            return redirect(reverse('login'), kwargs={'next':request.path})

        try:
            rating = int(request.POST.get('rating'))
        except ValueError:
            rating = 0
        discription = request.POST.get('message')

        if not discription:
            return handle_error(request, 'Please fill all fields !', fragment="commentForm")
        try:
            Comment.objects.create(
                commenter=request.user.cook,
                commented_to=recipe,
                discription=discription,
                rating=rating
            )
        except OperationalError:
            return handle_error(request, 'Sorry, Comment posting failed !', fragment="commentForm")
        except Exception:
            return handle_error(request, 'Sorry, Unexpected error occured !', fragment="commentForm")

    try:
        recipe.avg_rating = sum([comment.rating for comment in recipe.comments.all()]) // recipe.comments.count()
    except ZeroDivisionError as e:
        recipe.avg_rating = 0
    
    try:
        num_of_comments = int(request.GET.get('cmt', "4"))
    except ValueError:
        num_of_comments = 4
    comments = recipe.comments.order_by('-id')[:num_of_comments]
    comments.is_max = num_of_comments >= recipe.comments.count()
    return render(request, 'recipe/recipe-post.html', {'recipe': recipe, 'comments':comments})

@login_required
def like_or_dislike(request, target):
    target_recipe = get_object_or_404(Recipe, id=target)
    kitchen_book = request.user.cook.kitchen_book

    if not kitchen_book.favorite_recipes.contains(target_recipe):
        kitchen_book.favorite_recipes.add(target_recipe)
    else:
        kitchen_book.favorite_recipes.remove(target_recipe)

    return redirect(reverse('recipe_post', args=[target]))