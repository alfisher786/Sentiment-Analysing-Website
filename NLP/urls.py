from django.contrib import admin
from django.urls import path
from NLP import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='text'),
    path('text/', views.text, name='text'),
    path('tweet/', views.tweet, name='tweet'),
    path('contact/', views.contact, name='contact'),
    path('result/', views.result, name='result'),
    path('result2/', views.result2, name='result2')
    ]
