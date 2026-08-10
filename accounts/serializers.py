from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'fullname']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'fullname', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid Credentials")

        attrs['user'] = user
        return attrs

