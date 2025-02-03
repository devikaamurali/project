from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name="index"),
    path('login', views.login,name="login"),
    path('signup', views.signup,name="signup"),
    
]
