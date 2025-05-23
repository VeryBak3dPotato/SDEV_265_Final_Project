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
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

class BaseUserDetailView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication]

    def get_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise PermissionDenied("User not found.")
        return user

    def check_user_permissions(self, request, user):
        
        if not request.user.is_staff and request.user.id != user.id:
            raise PermissionDenied("You do not have permission to access this user's information.")

class UserDetailView(BaseUserDetailView):
    def get_geo_location(self, zip_code, api_key):
        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
        response = requests.get(url)
        return response.json()

    def get_weather_data(self, lat, lon, units, api_key):
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={units}&appid={api_key}"
        response = requests.get(url)
        return response.json()

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        if not user.zipCode:
            return Response({"error": "User does not have a valid zip code."}, status=HTTP_400_BAD_REQUEST)

        geo_location = self.get_geo_location(user.zipCode, settings.API_KEY)
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.UNITS, settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            # 'firstName': user.firstName,
            # 'lastName': user.lastName,
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
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.UNITS, settings.API_KEY)

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
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.UNITS, settings.API_KEY)

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
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.UNITS, settings.API_KEY)

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
        weather_data = self.get_weather_data(geo_location['lat'], geo_location['lon'], settings.UNITS, settings.API_KEY)

        content = {
            'id': user.id,
            'user': str(user),
            'zipCode': user.zipCode,
            'city': geo_location['name'],
            'dailyWeather': weather_data["daily"],
        }
        return Response(content)

class UpdateZipCodeView(UserDetailView):
    def put(self, request, pk, format=None):
        user = self.get_user(pk)
        self.check_user_permissions(request, user)

        new_zip_code = request.data.get("zipCode")

        if not new_zip_code:
            return Response({"error": "ZIP code is required."}, status=HTTP_400_BAD_REQUEST)

        user.zipCode = new_zip_code
        user.save()

        return Response({"success": "ZIP code updated successfully.", "zipCode": user.zipCode}, status=HTTP_200_OK)

class RegisterUser(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        required_fields = ["email", "password", "zipCode"]
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        
        if missing_fields:
            return Response({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=HTTP_400_BAD_REQUEST)

        password = request.data.get("password")
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # Set the provided password
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "success": "Successful registration",
                "token": token.key,
                "id": user.id,
                "email": user.email,
                # "firstName":user.firstName,
                # "lastName": user.lastName,
                "zipCode": user.zipCode
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        username = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "success": "Successful authentication",
                "token": token.key,
                "id": user.id
            }, status=HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def post(self, request):
        # Delete the user's token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=200)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=400)
        
class HelloWorldView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        return Response({"message": "Hello, World!"}, status=HTTP_200_OK)