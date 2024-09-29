"""
URL configuration for management project.

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
from django.urls import path
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', registerpage, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logut_page, name='logout'),
    path('events/', include('events.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
