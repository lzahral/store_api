from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'email', 'password']

    def validate_email(self, value):  # field level validation
        if User.objects.filter(email=value).first():
            raise serializers.ValidationError('User with the same email already exists ')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    

