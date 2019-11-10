from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'crawling'

urlpatterns = [
    path('', views.main, name='main'),
    path('crawling/', views.CrawlingStore, name='crawlingstore'),
    #path('crawling/pants/', PantsRecommendListView.as_view(), name='pants'),
]