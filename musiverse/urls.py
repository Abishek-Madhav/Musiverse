"""
URL configuration for musiverse project.

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
from musiverse_app import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('innovation/', views.innovation_page, name='innovation'),
    path('player/', views.player_page, name='player'),
    path('compose/', views.compose_page, name='compose'),
    path('lyric/', views.lyric_page, name='lyric'),
    path('generate/', views.generate_page, name='generate'),
    path('user-details/', views.get_user_details, name='user-details'),
    path('account/', views.account_page, name='account'),
]
