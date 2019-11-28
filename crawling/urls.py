from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'crawling'

urlpatterns = [
    path('', views.main, name='main'),
    path('personal/', views.PersonalStore, name='personalsize'),
    path('store/', views.CrawlingStore, name='crawlingstore'),
    #path('crawling/pants/', PantsRecommendListView.as_view(), name='pants'),
]