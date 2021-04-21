from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather, name = 'weather-home'),
    path('about/', views.about, name = 'weather-about')
]