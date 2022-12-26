from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from ads import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('api-auth/', include('rest_framework.urls')),
    path('cat/', include('ads.cat_urls')),
    path('ads/', include('ads.urls')),
    path('users/', include('ads.users_url')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
