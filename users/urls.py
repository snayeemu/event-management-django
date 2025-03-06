
from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('sign-up', views.sign_up, name="sign-up"),
]

