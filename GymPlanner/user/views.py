from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer
from .tasks import send_confirmation_email


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            token = default_token_generator.make_token(user)
            confirm_url = request.build_absolute_uri(
                reverse('confirm-email', kwargs={'uid': user.id, 'token': token})
            )
            send_confirmation_email.delay(user.email, confirm_url)
            return Response(
                {'message': 'Пользователь зарегистрирован. Проверьте вашу почту для подтверждения.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ConfirmEmailView(APIView):
    def get(self, request, uid, token):
        user = get_object_or_404(CustomUser, id=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Электронная почта успешно подтверждена."}, status=status.HTTP_200_OK)
        return Response({"message": "Недействительный или просроченный токен."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return Response(
                    {'detail': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not user.check_password(password):
                return Response(
                    {'detail': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not user.is_active:
                return Response(
                    {'detail': 'Аккаунт не подтвержден. Проверьте вашу почту.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)