"""
URL configuration for professional_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

app_name = 'config'
urlpatterns = [
    path('manage/', admin.site.urls),
    path('two_factor/', include(('admin_two_factor.urls', 'admin_two_factor'), namespace='two_factor')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('layout.urls'), name='index'),
    path('career/', include('career.urls'), name='career'),
    path('aboutme/', include('aboutme.urls'), name='aboutme'),
    path('contactme/', include('contactme.urls'), name='contactme'),
    path('blog/', include('blog.urls'), name='blog'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
