from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from .serializers import (
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
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


@extend_schema(tags=['Authentication'])
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.get_user()

        if user:
            # Generate token and send email
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Construct the reset link (adjust the domain and frontend URL as needed)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/" # Example frontend URL structure

            subject = 'Password Reset Request'
            message = render_to_string('emails/password_reset_email.txt', {
                'user': user,
                'reset_link': reset_link,
            })
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, message, email_from, recipient_list)

        # Always return a success response to prevent email enumeration
        return Response({'detail': 'Password reset email sent if email is registered.'}, status=status.HTTP_200_OK)

@extend_schema(tags=['Authentication'])
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)