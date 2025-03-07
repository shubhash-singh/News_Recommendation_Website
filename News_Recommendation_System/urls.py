"""News_Recommendation_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.shortcuts import render

from .views import login_view
from .views import signup_view
from .views import top_news_view
from .views import recommended_news
from .views import like_from_user_view
from .views import update_category_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, 'index.html')),
    path('login/',login_view, name="login"),
    path('signup/',signup_view, name='signup'),
    path('top_news/',top_news_view, name="top_news"),
    path("recommended_news/", recommended_news, name="recommended_news"),
    path("like_news/", like_from_user_view, name="like_news"),
    path("update_categories/", update_category_view, name="update_categories")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
