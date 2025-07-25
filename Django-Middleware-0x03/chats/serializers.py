from rest_framework import serializers
from django.conf import settings
from .models import Conversation, Message
from django.contrib.auth import get_user_model


# Reference the custom user model via settings.AUTH_USER_MODEL

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'phone_number', 'full_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    # ✅ now it's not required in input
    conversation = serializers.UUIDField(read_only=True)
    preview = serializers.CharField(source='message_body', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender',
                  'message_body', 'sent_at', 'preview']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        many=True,
        slug_field='username'
    )
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, data):
        if self.instance is None and len(data.get('participants', [])) < 1:
            raise serializers.ValidationError(
                "A conversation must have at least one other participant."
            )
        return data

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']
