from rest_framework import serializers
from .models import ConstructedCollection, UserConstructedCollection


class ConstructedCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructedCollection
        fields = "__all__"


class ConstructedCollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructedCollection
        fields = ("name", "collection_image", "status")


class UserConstructedCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructedCollection
        fields = "__all__"


class UserConstructedCollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConstructedCollection
        fields = ("user", "constructed_collection")
