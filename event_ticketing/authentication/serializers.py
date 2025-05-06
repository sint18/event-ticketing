from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "role")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserRegistrationSerializer, self).create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Set the username field to 'email'
    username_field = "email"


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password.")
        return value

    def save(self):
        user = self.context["request"].user
        # Set the new password (Django's set_password handles hashing)
        user.password = make_password(self.validated_data["new_password"])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            # We don't raise a ValidationError here to prevent revealing
            # whether an email address exists in the system.
            return value
        return value

    def get_user(self):
        email = self.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'uidb64': ['Invalid value']})

        token = data['token']
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({'token': ['Invalid or expired token']})

        self.user = user
        return data

    def save(self):
        # Set the new password for the user
        self.user.password = make_password(self.validated_data['new_password'])
        self.user.save()
        return self.user
