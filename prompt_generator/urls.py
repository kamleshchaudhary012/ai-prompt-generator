"""
URL configuration for prompt_generator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import FileResponse
import os

def serve_robots_txt(request):
    file_path = settings.ROBOTS_TXT_PATH
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    return FileResponse(open(os.path.join(settings.STATIC_ROOT, 'robots.txt'), 'rb'), content_type='text/plain')

def serve_sitemap_xml(request):
    file_path = settings.SITEMAP_XML_PATH
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/xml')
    return FileResponse(open(os.path.join(settings.STATIC_ROOT, 'sitemap.xml'), 'rb'), content_type='application/xml')

def serve_ads_txt(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'ads.txt')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    return FileResponse(open(os.path.join(settings.STATIC_ROOT, 'ads.txt'), 'rb'), content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('generator.urls')),
    path('robots.txt', serve_robots_txt),
    path('sitemap.xml', serve_sitemap_xml),
    path('ads.txt', serve_ads_txt),
]
