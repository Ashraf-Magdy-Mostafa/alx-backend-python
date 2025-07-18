from rest_framework import serializers
from django.conf import settings
from .models import Conversation, Message

# Reference the custom user model via settings.AUTH_USER_MODEL
User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Exposes core user fields.
    """
    class Meta:
        model = User
        # You can customize fields but typical useful subset:
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Displays sender as username via StringRelatedField.
    """
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Participants serialized via UserSerializer (many=True).
    Nested messages included with MessageSerializer.
    Both read-only to ensure messages and participants are managed separately.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']
