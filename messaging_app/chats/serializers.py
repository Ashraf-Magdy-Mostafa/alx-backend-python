from rest_framework import serializers
from django.conf import settings
from .models import Conversation, Message

# Reference the custom user model via settings.AUTH_USER_MODEL
User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Exposes core user fields.
    Adds a computed full_name field using SerializerMethodField.
    """
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'phone_number', 'full_name']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Displays sender as username via StringRelatedField.
    Adds a CharField for message preview (first 30 chars).
    """
    sender = serializers.StringRelatedField(read_only=True)
    preview = serializers.CharField(source='message_body', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender',
                  'message_body', 'sent_at', 'preview']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Participants serialized via UserSerializer (many=True).
    Nested messages included with MessageSerializer.
    Adds validation to ensure at least two participants.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, data):
        if self.instance is None and len(data.get('participants', [])) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants.")
        return data

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']
