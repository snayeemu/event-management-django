
from django.contrib import admin
from django.urls import path, include
from events import views

urlpatterns = [
    path('', views.event_list, name="event-list"),
    path('events/<int:pk>/', views.event_details, name="event-details"),
    path('events/create/', views.event_create, name="event-create"),
    path('events/<int:pk>/update/', views.event_update, name="event-update"),
    path('events/<int:pk>/delete/', views.event_delete, name="event-delete"),
    path('events/<int:pk>/details/', views.event_details, name="event-details"),

    path('participants/', views.participant_list, name='participant-list'),
    path('participants/create/', views.participant_create, name='participant-create'),
    path('participants/<int:pk>/update/', views.participant_update, name='participant-update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant-delete'),
    
    path('categories/', views.category_list, name='category-list'),
    path('categories/create', views.category_create, name='category-create'),
    path('categories/<int:pk>/update', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete', views.category_delete, name='category-delete'),
    path('dashboard/organizer', views.organizer_dashboard, name='organizer-dashboard'),
]

