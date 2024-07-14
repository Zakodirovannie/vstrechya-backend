import base64


from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny


from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.settings import DJOSER
from core.utils import upload_image, send_activation_email_task


from .pipeline import set_jwt_cookies
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ["user_edit_get", "user_edit_post", "upload_avatar"]:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return tuple(permission() for permission in self.permission_classes)

    @action(detail=True)
    def user_get(self, request, *args, **kwargs):
        User = get_user_model()
        self.object = get_object_or_404(User, pk=kwargs["pk"])
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(detail=True)
    def user_me(self, request):
        if request.user.is_authenticated:
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(permission_classes=(IsAuthenticated,), detail=True)
    def user_edit_get(self, request, *args, **kwargs):
        User = get_user_model()
        self.object = get_object_or_404(User, pk=kwargs["pk"])
        serializer = UserEditSerializer(self.object)
        return Response(serializer.data)

    @action(permission_classes=(IsAuthenticated,), detail=True)
    def user_edit_post(self, request, *args, **kwargs):
        if request.user.id and kwargs["pk"] == request.user.id:
            data = request.data
            serializer = self.serializer_class(data=data, partial=True)
            if serializer.is_valid():
                serializer.update(instance=request.user, validated_data=data)
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(permission_classes=(IsAuthenticated,), detail=True, methods=["post"])
    def upload_avatar(self, request, *args, **kwargs):
        img = request.data.get("img")
        if img:
            image_url = upload_image.delay(
                base64.b64encode(img.read()), "avatars", True
            )
            user = request.user
            user.image_url = image_url.wait(timeout=None, interval=0.5)
            user.save()
            return Response({"image_url": user.image_url}, status=status.HTTP_200_OK)
        return Response({"img": "no image"}, status=status.HTTP_400_BAD_REQUEST)

    # !ONLY FOR CHAT APP!
    @action(permission_classes=(IsAuthenticated,), detail=False)
    def all(self, request):

        serializer = UserCreateSerializer(self.queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


User = get_user_model()


class SendActivationEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return Response(
                {"detail": "Пользователь уже активирован."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        activation_link = DJOSER["ACTIVATION_URL"].format(uid=uid, token=token)
        context = {
            "user_id": user.id,
            "url": activation_link,
            "protocol": "https" if request.is_secure() else "http",
            "domain": request.get_host(),
        }

        send_activation_email_task.delay(context, [user.email])

        return Response(
            {"detail": "Активационное письмо отправлено."}, status=status.HTTP_200_OK
        )


#class CustomActivationEmail(ActivationEmail):
    #template_name = "activation_email.html"


class ActivationView(APIView):
    def get(self, request, uid, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"status": "Аккаунт успешно активирован"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "Ошибка активации аккаунта"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            tokens = {
                "access": response.data.get("access"),
                "refresh": response.data.get("refresh"),

            }
            set_jwt_cookies(response, tokens, request)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            tokens = {
                "access": response.data.get("access"),
                "refresh": response.data.get("refresh"),

            }
            set_jwt_cookies(response, tokens, request)
        return response
