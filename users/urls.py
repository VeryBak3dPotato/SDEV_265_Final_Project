from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('weather/<int:pk>/current/', WeatherCurrentView.as_view(), name='weather-current'),
    path('weather/<int:pk>/minutely/', WeatherMinutelyView.as_view(), name='weather-minutely'),
    path('weather/<int:pk>/hourly/', WeatherHourlyView.as_view(), name='weather-hourly'),
    path('weather/<int:pk>/daily/', WeatherDailyView.as_view(), name='weather-daily'),
    path('weather/<int:pk>/update-zip/', UpdateZipCodeView.as_view(), name='update-zip'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
