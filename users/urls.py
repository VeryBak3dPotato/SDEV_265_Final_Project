from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/current/', WeatherCurrentView.as_view(), name='weather-current'),
    path('users/<int:pk>/minutely/', WeatherMinutelyView.as_view(), name='weather-minutely'),
    path('users/<int:pk>/hourly/', WeatherHourlyView.as_view(), name='weather-hourly'),
    path('users/<int:pk>/daily/', WeatherDailyView.as_view(), name='weather-daily'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('hello/', HelloView.as_view(), name='hello'),
]
