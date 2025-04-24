from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer

class UserListView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get(self, request, format=None):
        users = User.objects.all()  # Fetch all users
        serializer = self.serializer_class(users, many=True)  # Serialize the users
        return Response(serializer.data)  # Return serialized data

class UserDetailView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def get(self, request, pk, format=None):
        # Allow admin users to view any user's details
        if not request.user.is_staff and request.user.id != int(pk):
            raise PermissionDenied(
                "You do not have permission to access this user's information."
            )
        
        # Fetch the user object based on the primary key
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {
                    "error": "User not found."
                },
                status=404
            )

        content = {
            'id': user.id,
            'user': str(user),
            'firstName': user.firstName,
            'lastName': user.lastName,
            'zipCode': user.zipCode,
        }
        return Response(content)

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