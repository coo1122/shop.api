from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserBaseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
    email = serializers.EmailField()

class UserAuthSerializer(UserBaseSerializer):
    pass

class UserRegisterSerializer(UserBaseSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('Username already exists!')

class SMSCodeSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(max_length=6)