from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Message, Conversation, ConversationUser
from account.serializers import UsersCreateSerializer

User = get_user_model()


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name", "other_user", "last_message")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data

    def get_other_user(self, obj):
        usernames = obj.name.split("__")
        context = {}
        for username in usernames:
            if int(username) != self.context["user"].id:
                # This is the other participant
                other_user = User.objects.get(id=int(username))
                return UsersCreateSerializer(other_user, context=context).data


class ConversationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationUser
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "content",
            "timestamp",
            "read",
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)

    def get_from_user(self, obj):
        return UsersCreateSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return UsersCreateSerializer(obj.to_user).data
