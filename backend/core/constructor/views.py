import base64
import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ConstructedCollection, UserConstructedCollection
from .serializers import (
    ConstructedCollectionSerializer,
    ConstructedCollectionCreateSerializer,
    UserConstructedCollectionCreateSerializer,
)
from core.utils import upload_image
from .permissions import IsActiveUser


class ConstructedCollectionViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in [
            "create_collection_get",
            "create_collection_post",
            "update_collection_content",
            "upload_image",
            "delete_collection",
        ]:
            self.permission_classes = [IsAuthenticated, IsActiveUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ["create_collection_get", "create_collection_post"]:
            return ConstructedCollectionCreateSerializer
        return ConstructedCollectionSerializer

    @action(detail=True)
    def get_collection_by_id(self, request, *args, **kwargs):
        collection_id = kwargs.get("pk")
        collection = get_object_or_404(ConstructedCollection, id=collection_id)
        serializer = ConstructedCollectionSerializer(collection)
        return Response(serializer.data)

    @action(detail=False)
    def create_collection_get(self, request, *args, **kwargs):
        return Response({"name": ""})

    @csrf_exempt
    def upload_image(self, request, *args, **kwargs):
        img = request.FILES.get("img")
        if img:
            url = upload_image.apply_async(
                (base64.b64encode(img.read()), "collection_images/avatars", True)
            ).get()
            return Response({"image_url": url}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Картинка не отправлена"}, status=status.HTTP_400_BAD_REQUEST
        )

    @csrf_exempt
    @action(detail=False)
    def create_collection_post(self, request, *args, **kwargs):
        data = request.data.copy()
        img = request.data.get("collection_image")
        if img:
            image_url = upload_image.delay(
                base64.b64encode(img.read()), "collection_images/avatars", True
            )
            data["collection_image"] = image_url.wait(timeout=None, interval=0.5)

        try:
            if data["json_data"] is not None:
                try:
                    data["json_data"] = json.loads(data["json_data"])
                except:
                    return Response({"detail": "Неверные данные JSON формата"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ConstructedCollectionCreateSerializer(data=data)
        if serializer.is_valid():
            collection = serializer.save()

            user_collection_data = {
                "user": request.user.id,
                "constructed_collection": collection.id,
            }
            user_collection_serializer = UserConstructedCollectionCreateSerializer(
                data=user_collection_data
            )
            if user_collection_serializer.is_valid():
                user_collection_serializer.save()
                full_collection_serializer = ConstructedCollectionSerializer(collection)
                return Response(
                    full_collection_serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                user_collection_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    @action(detail=True, methods=["patch"])
    def update_collection_content(self, request, pk=None):
        collection = get_object_or_404(ConstructedCollection, pk=pk)

        json_data = request.data.get("json_data")
        html_content = request.data.get("html_content")

        try:
            if json_data is not None:
                try:
                    json_data = json.loads(json_data)
                except:
                    return Response({"detail": "Неверные данные JSON формата"}, status=status.HTTP_400_BAD_REQUEST)
                collection.json_data = json_data
            if html_content is not None:
                collection.html_content = html_content
            collection.save()
            return Response(
                {"detail": "Обновление прошло успешно"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    @action(detail=True, methods=["delete"])
    def delete_collection(self, request, pk=None):
        collection = get_object_or_404(ConstructedCollection, pk=pk)
        user_collection = get_object_or_404(
            UserConstructedCollection, constructed_collection=collection
        )

        if user_collection.user != request.user:
            return Response(
                {"detail": "Вы не являетесь владельцем этой коллекции"},
                status=status.HTTP_403_FORBIDDEN,
            )

        collection.delete()
        return Response(
            {"detail": "Коллекция успешно удалена"}, status=status.HTTP_204_NO_CONTENT
        )
