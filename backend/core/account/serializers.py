from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from collection.models import UserCollection, Collection
from collection.serializers import UserCollectionSerializer
from constructor.models import UserConstructedCollection, ConstructedCollection
from constructor.serializers import UserConstructedCollectionSerializer

User = get_user_model()


class UsersCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "image_url",
            "created_at",
            "updated_at",
            "phone",
        )


class UserDetailSerializer(UserSerializer):
    collections = serializers.SerializerMethodField()
    exhibitions = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "image_url",
            "phone",
            "collections",
            "exhibitions"
        )

    def get_collections(self, user):
        user_collections = UserCollection.objects.filter(user=user)

        collections = []

        for coll in user_collections:
            collections.append(
                UserCollectionSerializer(
                    Collection.objects.get(id=coll.collection.id)
                ).data
            )

        return collections

    def get_exhibitions(self, user):
        user_constructed_collections = UserConstructedCollection.objects.filter(
            user=user
        )
        exhibitions = []

        for constructed_coll in user_constructed_collections:
            exhibitions.append(
                UserConstructedCollectionSerializer(
                    ConstructedCollection.objects.get(
                        id=constructed_coll.constructed_collection.id
                    )
                ).data
            )

        return exhibitions


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "image_url",
            "id",
        )
