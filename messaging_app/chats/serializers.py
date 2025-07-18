from rest_framework import serializers
from django.conf import settings  # To get the AUTH_USER_MODEL
from .models import Conversation, Message  # Import your models

# Assuming your custom user model is named CustomUser in users/models.py
# You might need to adjust the import path based on your project structure.
# For simplicity, we'll refer to it via settings.AUTH_USER_MODEL.


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    This serializer will expose basic user information.
    """


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes the sender's username for readability.
    """
    # Use StringRelatedField to display the username of the sender
    sender = serializers.StringRelatedField(read_only=True)
    # Alternatively, if you need more sender details, you could nest the UserSerializer:
    # sender = UserSerializer(read_only=True)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Handles the many-to-many relationship for participants and
    nests messages within the conversation.
    """
    # Use UserSerializer to represent participants, allowing for more detail than just IDs.
    # many=True is required for ManyToManyField.
    participants = UserSerializer(many=True, read_only=True)

    # Nest the MessageSerializer to display all messages within this conversation.
    # many=True is required as there can be multiple messages.
    # read_only=True means messages cannot be created/updated directly through this serializer.
    # To create messages, you'd typically use the MessageSerializer directly.
    messages = MessageSerializer(many=True, read_only=True)
