from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    PasswordChangeSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
)


@extend_schema(tags=["Authentication"])
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Allow anyone to register
    serializer_class = UserRegistrationSerializer


@extend_schema(tags=["Authentication"])
class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can change their password

    # The UpdateAPIView expects to update a model instance,
    # but we're updating the authenticated user directly.
    # We can override get_object to return the current user.
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Use the serializer's save method to handle the password change
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    # Use your custom serializer for this view
    serializer_class = CustomTokenObtainPairSerializer
