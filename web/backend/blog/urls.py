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
from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogView.as_view(), name='blog'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('<slug:slug>/', views.ArticleView.as_view(), name='article'),
    path('tag/<slug:tag>/', views.TagView.as_view(), name='tag'),
    path('date/<slug:date>/', views.DateView.as_view(), name='date')
]
