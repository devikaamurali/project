from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name="index"),
    path('login/', views.login,name="login"),
    path('signup/', views.signup,name="signup"),
    path('about/', views.about,name="about"),
    path('feedback/', views.feedback,name="feedback"),
    path('verify/', views.verify,name="verify"),
    path("check-url/", views.check_url_validity, name="check_url_validity"),
]
