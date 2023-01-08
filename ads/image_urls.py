from django.contrib import admin
from django.urls import path
from rest_framework import routers
from ads import views
from ads.views import AdsViewSet

urlpatterns = [

    # path('', views.AdsListViews.as_view()),
    # path('<int:pk>/', views.AdsDetailView.as_view()),
    # path('create/', views.AdsCreateView.as_view()),
    # path('<int:pk>/update/', views.AdsUpdateView.as_view()),
    # path('<int:pk>/delete/', views.AdsDeleteView.as_view()),
    path('<int:pk>/image/', views.AdsImageView.as_view()),
]

router = routers.SimpleRouter()
router.register('', AdsViewSet)

urlpatterns += router.urls
