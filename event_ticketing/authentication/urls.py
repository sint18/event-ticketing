from django.urls import path
from .views import PasswordChangeView, PasswordResetConfirmView, PasswordResetRequestView, UserRegistrationView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path(
        "token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT Login
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # JWT Refresh
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password/reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
