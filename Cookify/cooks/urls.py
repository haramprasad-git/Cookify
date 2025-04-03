from django.urls import path 
from . import views

urlpatterns = [
    path('cook/login/', views.login, name='login'),
    path('cook/add/', views.signup, name='signup'),
    path('cook/profile', views.show_profile, name='cook_profile')
]