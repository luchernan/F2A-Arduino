# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from authiot.views import index_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authiot.urls')),
    path('', index_view, name='index'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
