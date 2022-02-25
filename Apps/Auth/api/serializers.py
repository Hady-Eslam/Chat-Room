from rest_framework import serializers
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class ForgetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=1, max_length=100, required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=1, max_length=100, required=True, write_only=True)
