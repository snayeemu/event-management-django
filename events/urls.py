
from django.contrib import admin
from django.urls import path, include
from events import views

urlpatterns = [
    path("cards/", views.event_cards, name="event-cards"),
    path('<int:pk>/', views.event_details, name="event-details"),
    path('create/', views.event_create, name="event-create"),
    path('<int:pk>/update/', views.event_update, name="event-update"),
    path('<int:pk>/delete/', views.event_delete, name="event-delete"),
    path('<int:pk>/details/', views.event_details, name="event-details"),
    path('rsvp/<int:id>/', views.rsvp, name="rsvp"),

    path('participants/', views.participant_list, name='participant-list'),
    path('participants/<int:pk>/update/', views.participant_update, name='participant-update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant-delete'),
    
    path('categories/', views.category_list, name='category-list'),
    path('categories/create', views.category_create, name='category-create'),
    path('categories/<int:pk>/update', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete', views.category_delete, name='category-delete'),

    path('dashboard/organizer', views.organizer_dashboard, name='organizer-dashboard'),
    path('dashboard/admin', views.admin_dashboard, name='admin-dashboard'),
]

