from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add/', views.signup, name='signup'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('edit/password/', views.change_password, name='change_password'),
    path('profile/<id>/', views.show_profile, name='cook_profile'),
    path('follow/unfollow/<target>/', views.follow_or_unfollow, name='follow_or_unfollow'),
    path('kitchenbook/', views.show_kitchen_book, name='kitchen_book')
]