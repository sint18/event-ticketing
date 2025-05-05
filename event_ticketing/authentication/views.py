from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from .models import User
from .serializers import UserRegistrationSerializer


@extend_schema(tags=["Authentication"])
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Allow anyone to register
    serializer_class = UserRegistrationSerializer
