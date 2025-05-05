from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
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
