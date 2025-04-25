from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.conf import settings
from .models import User
from .serializers import UserSerializer
import requests

class UserListView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get(self, request, format=None):
        users = User.objects.all()  # Fetch all users
        serializer = self.serializer_class(users, many=True)  # Serialize the users
        return Response(serializer.data)  # Return serialized data

class BaseUserDetailView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get_user(self, pk):
        # Fetch the user object based on the primary key
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise PermissionDenied("User not found.")
        return user

    def check_user_permissions(self, request, user):
        # Allow admin users to view any user's details
        if not request.user.is_staff and request.user.id != user.id:
            raise PermissionDenied("You do not have permission to access this user's information.")

class UserDetailView(BaseUserDetailView):
    def get_geo_location(self, zip_code, api_key):
        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
        response = requests.get(url)
        return response.json()

    def get_weather_data(self, lat, lon, api_key):
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        return response.json()

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        if not user.zipCode:
            return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)

        geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            'firstName': user.firstName,
            'lastName': user.lastName,
            'zipCode': user.zipCode,
            'city': geo_location['name'],
            'allWeather': weather_data,
        }
        return Response(content)

class WeatherCurrentView(UserDetailView):
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        if not user.zipCode:
            return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)
        
        geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            'zipCode': user.zipCode,
            'city': geo_location['name'],
            'currentWeather': weather_data["current"],
        }
        return Response(content)

class WeatherMinutelyView(UserDetailView):
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        if not user.zipCode:
            return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)
        
        geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            'zipCode': user.zipCode,
            'city': geo_location['name'],
            'minutelyWeather': weather_data["minutely"],
        }
        return Response(content)

class WeatherHourlyView(UserDetailView):
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        if not user.zipCode:
            return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)
        
        geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            'zipCode': user.zipCode,
            'city': geo_location['name'],
            'hourlyWeather': weather_data["hourly"],
        }
        return Response(content)
    
class WeatherDailyView(UserDetailView):
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        if not user.zipCode:
            return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)
        
        geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            'zipCode': user.zipCode,
            'city': geo_location['name'],
            'dailyWeather': weather_data["daily"],
        }
        return Response(content)

# class WeatherMinutelyView(BaseUserDetailView):
#     def get_geo_location(self, zip_code, api_key):
#         url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
#         response = requests.get(url)
#         return response.json()

#     def get_weather_data(self, lat, lon, api_key):
#         url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid={api_key}"
#         response = requests.get(url)
#         return response.json()

#     def get(self, request, pk, format=None):
#         user = self.get_user(pk)
#         self.check_user_permissions(request, user)

#         if not user.zipCode:
#             return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)

#         geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
#         weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.API_KEY)

#         content = {
#             'id': user.id,
#             'user': str(user),
#             'zipCode': user.zipCode,
#             'weatherData': weather_data,
#         }
#         return Response(content)



# class UserDetailView(APIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

#     def get(self, request, pk, format=None):
#         # Allow admin users to view any user's details

#         if not request.user.is_staff and request.user.id != int(pk):
#             raise PermissionDenied(
#                 "You do not have permission to access this user's information."
#             )
        
#         # Fetch the user object based on the primary key
#         try:
#             user = User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response(
#                 {
#                     "error": "User not found."
#                 },
#                 status=404
#             )

#         def get_geo_location(zip_code, api_key):
#             url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
#             geo_loaction = requests.get(url)
#             return geo_loaction.json()
        
#         def get_weather_data(lat, lon, api_key):
#             url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
#             weather_data = requests.get(url)
#             return weather_data.json()
        
#         if not user.zipCode:
#             return Response(
#                 {"error": "User does not have a valid zip code."},
#                 status=HTTP_400_BAD_REQUEST
#             )
        
#         geo_loaction = get_geo_location(user.zipCode, settings.API_KEY)
#         weather_data = get_weather_data(geo_loaction['lat'], geo_loaction['lon'], settings.API_KEY)

#         content = {
#             'id': user.id,
#             'user': str(user),
#             'firstName': user.firstName,
#             'lastName': user.lastName,
#             'zipCode': user.zipCode,
#             'weatherData': weather_data,
#         }
#         return Response(content)
    
# class WeatherCurrentView(APIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

#     def get(self, request, pk, format=None):
#         # Allow admin users to view any user's details

#         if not request.user.is_staff and request.user.id != int(pk):
#             raise PermissionDenied(
#                 "You do not have permission to access this user's information."
#             )
        
#         # Fetch the user object based on the primary key
#         try:
#             user = User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response(
#                 {
#                     "error": "User not found."
#                 },
#                 status=404
#             )

#         def get_geo_location(zip_code, api_key):
#             url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
#             geo_loaction = requests.get(url)
#             return geo_loaction.json()
        
#         def get_weather_data(lat, lon, api_key):
#             url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid={api_key}"
#             weather_data = requests.get(url)
#             return weather_data.json()
        
#         if not user.zipCode:
#             return Response(
#                 {"error": "User does not have a valid zip code."},
#                 status=HTTP_400_BAD_REQUEST
#             )
        
#         geo_loaction = get_geo_location(user.zipCode, settings.API_KEY)
#         weather_data = get_weather_data(geo_loaction['lat'], geo_loaction['lon'], settings.API_KEY)

#         content = {
#             'weatherData': weather_data,
#         }
#         return Response(content)

# class WeatherHourlyView(APIView):
#     pass

# class WeatherDailyView(APIView):
#     pass

class RegisterUser(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True  # Ensure the user is active by default
            user.save()  # Save the updated user instance
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
        
class BasicView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        return Response({"message": "Hello, world!"}, status=HTTP_200_OK)