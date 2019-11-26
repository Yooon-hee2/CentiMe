"""capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views

app_name = 'recommend'

urlpatterns = [
    path('', views.recommend_main, name = 'main'),
    path('recent/', views.recent_recommend, name = 'recent_item'),
    path('trend/', views.trend_recommend, name = 'trend_item'),
    path('all/', views.all_list, name='all'),
    #path('crawling/pants/', PantsRecommendListView.as_view(), name='pants'),
]