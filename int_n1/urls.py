"""int_n1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from main.views import RegisterView,no_posts,posts,all_posts,Login

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', home),
    path('auth/login/', Login.as_view()),
    path('auth/register/', RegisterView.as_view()),
    path(r'details/author/<id>', no_posts),
    path(r'details/posts/<id>', posts),
    path(r'posts', all_posts)
]
