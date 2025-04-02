from django.contrib import admin
from .models import Category, Recipe, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Comment)