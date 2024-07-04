from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Collection, UserCollection
from rest_framework import serializers
from .models import CollectionItem

User = get_user_model()


class UserCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class CollectionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItem
        fields = "__all__"


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class UserCollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollection
        fields = ("user", "collection")
