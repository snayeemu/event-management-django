
from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('sign-up', views.sign_up, name="sign-up"),
    path('sign-in', views.sign_in, name="sign-in"),
    path('sign-out', views.sign_out, name="sign-out"),
    path("create-group/", views.create_group, name="create-group"),
    path("activate/<int:user_id>/<str:token>/", views.activate_user),
    path("update/<int:id>/group/", views.update_group, name="update-group"),
    path("delete/<int:id>/group/", views.delete_group, name="delete-group"),
]

