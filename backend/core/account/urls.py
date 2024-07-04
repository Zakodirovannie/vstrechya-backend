from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import ActivationView, SendActivationEmailView
from django.urls import path, reverse_lazy
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = "account"

urlpatterns = [
    path("auth/signup/", UserViewSet.as_view({"post": "create"}), name="register"),
    path("auth/signin/", TokenObtainPairView.as_view(), name="create-token"),
    path("auth/api/token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("users/me/", views.UserViewSet.as_view({"get": "user_me"}), name="user-me"),
    path(
        "users/all/", views.UserViewSet.as_view({"get": "all"}), name="all"
    ),  # !ONLY FOR CHAT APP!
    path(
        "users/<int:pk>/edit",
        views.UserViewSet.as_view({"get": "user_edit_get", "post": "user_edit_post"}),
        name="edit",
    ),
    path(
        "users/<int:pk>/",
        views.UserViewSet.as_view({"get": "user_get"}),
        name="user_detail",
    ),
    path(
        "users/upload_avatar/",
        views.UserViewSet.as_view({"post": "upload_avatar"}),
        name="upload_avatar",
    ),
    path(
        "reset/password-reset/",
        PasswordResetView.as_view(
            email_template_name="./password_reset_email.html",
            success_url=reverse_lazy("account:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "reset/password-reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("account:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/password-reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("auth/activate/<uid>/<token>/", ActivationView.as_view(), name="activation"),
    path(
        "auth/send-activation-email/",
        SendActivationEmailView.as_view(),
        name="send_activation_email",
    ),
]
