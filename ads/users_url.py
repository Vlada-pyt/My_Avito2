from django.contrib import admin
from django.urls import path

from ads import views



urlpatterns = [
    path('', views.UsersListViews.as_view()),
    path('<int:pk>/', views.UsersDetailView.as_view()),
    path('create/', views.UsersCreateView.as_view()),
    path('<int:pk>/update/', views.UsersUpdateView.as_view()),
    path('<int:pk>/delete/', views.UsersDeleteView.as_view()),
]