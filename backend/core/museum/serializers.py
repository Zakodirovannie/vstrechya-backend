from rest_framework import serializers

from .models import Museum, MuseumUser


class MuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Museum
        fields = "__all__"


class MuseumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuseumUser
        fields = "__all__"
