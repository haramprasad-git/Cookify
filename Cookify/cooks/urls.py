from django.urls import path 
from . import views

urlpatterns = [
    path('cook/login/', views.login, name='login'),
    path('cook/logout/', views.logout, name='logout'),
    path('cook/add/', views.signup, name='signup'),
    path('cook/profile/<id>/', views.show_profile, name='cook_profile'),
    path('cook/follow/unfollow/<target>/', views.follow_or_unfollow, name='follow_or_unfollow')
]