from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.WeatherApiView.as_view(), name='weather_api'),
]
