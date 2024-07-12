from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from rest_framework_simplejwt.tokens import RefreshToken
import datetime

def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
        elif not user:
            user = social.user
    return {
        "social": social,
        "user": user,
        "is_new": user is None,
        "new_association": False,
    }


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return tokens


def set_jwt_cookies(response, tokens):
    response.set_cookie(
        key="access_token",
        value=tokens["access"],
        max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        httponly=True,
        secure=True,
        samesite='None',
        domain=".vstrechya.space",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh"],
        max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        httponly=True,
        secure=True,
        samesite='None',
        domain=".vstrechya.space",
    )


def completed(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.is_authenticated:
        response = HttpResponseRedirect("/users/me/")
        tokens = generate_jwt_token(user)
        set_jwt_cookies(response, tokens)
        return response
