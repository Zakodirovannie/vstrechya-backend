
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect

from rest_framework_simplejwt.tokens import RefreshToken

from .views import set_jwt_cookies
import logging

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import MissingBackend
from social_core.pipeline.partial import partial
from social_django.utils import load_backend, load_strategy
from social_django.views import complete as social_complete
from .views import set_jwt_cookies

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

@login_required
def completed(request, *args, **kwargs):
    user = request.user
    tokens = generate_jwt_token(user)
    response = redirect("http://localhost:8010/users/me/")
    set_jwt_cookies(response, tokens)
    return response
