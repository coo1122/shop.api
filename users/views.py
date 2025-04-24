from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserAuthSerializer, SMSCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from django.core.mail import send_mail
from . import models
from rest_framework.authtoken.views import APIView


class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(request.user)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'User credential are wrong!'})

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']
        is_active = False

        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        is_active=False)

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])

        models.SMSCode.objects.create(code=code, user=user)

        send_mail(
            'Registration code',
            message=code,
            from_email='<EMAIL>',
            recipient_list=[user.email]
        )

        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id})

class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = SMSCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        sms_code = serializer.validated_data.get('sms_code')
        try:
            sms_code = models.SMSCode.objects.get(code=sms_code)
        except models.SMSCode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Code not found'})

        sms_code.user.is_active = True
        sms_code.user.save()
        sms_code.delete()

        return Response(status=status.HTTP_200_OK)