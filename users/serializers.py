from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstName', 'lastName', 'zipCode', 'is_staff', 'is_active']