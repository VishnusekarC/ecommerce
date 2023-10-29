from django.contrib.auth import authenticate, logout
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUserAddress, CustomUserDetail
from .serializers.login_serializer import LoginSerializer
from .serializers.register_serializer import RegisterSerializer
from .serializers.user_address_serializer import (CreateUserAddressSerializer,
                                                  UserAddressSerializer)
from .serializers.user_detail_serializer import (
    CreateCustomUserDetailSerializer, GenericCustomUserDetailSerializer)
from .utils import send_email_to_user

# Authentication(Register, Login, Logout)


class RegisterUserAPIView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            send_email_to_user(user=user)
            return Response({"message": "sent activation mail to your account!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if not user:
                return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'Logged in success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


# Users

class CreateUserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUserDetail.objects.all()

    def post(self, request):
        try:
            _ = CustomUserDetail.objects.get(user=request.user)
            return Response({'message': 'User detail for the user already exist'}, status=status.HTTP_409_CONFLICT)
        except CustomUserDetail.DoesNotExist:
            serializer = CreateCustomUserDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(request.user, serializer.validated_data)
                return Response({'message': 'Details created success!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveCustomUserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_detail = CustomUserDetail.objects.get(user=request.user)
            serializer = GenericCustomUserDetailSerializer(
                user_detail, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUserDetail.DoesNotExist:
            return Response({'message': 'Detail Unavailable!'}, status=status.HTTP_404_NOT_FOUND)


class CreateUserAddressAPIView(generics.CreateAPIView):
    queryset = CustomUserAddress.objects.all()
    serializer_class = CreateUserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data


class GetMyAddressesAPIView(generics.ListAPIView):
    queryset = CustomUserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
