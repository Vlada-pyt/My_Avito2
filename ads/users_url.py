from django.contrib import admin
from django.urls import path
from rest_framework import routers
from ads import views
from ads.views import LocationViewSet

urlpatterns = [
    path('', views.UsersListViews.as_view()),
    path('<int:pk>/', views.UsersDetailView.as_view()),
    path('create/', views.UsersCreateView.as_view()),
    path('<int:pk>/update/', views.UsersUpdateView.as_view()),
    path('<int:pk>/delete/', views.UsersDeleteView.as_view()),
]


router = routers.SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns += router.urls