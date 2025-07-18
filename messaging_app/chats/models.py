import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

"""" Create a CustomUser Class that build upon existing User"""


class CustomUser(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    """
    # A unique identifier for the conversation.
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the conversation"
    )
    # Many-to-many relationship with the CustomUser model.
    # This tracks all participants in the conversation.
    # We use settings.AUTH_USER_MODEL to refer to the custom user model.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text="Users participating in this conversation"
    )


class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    # A unique identifier for the message.
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the message"
    )

    # Foreign key to the CustomUser model, representing the sender of the message.
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # If the sender is deleted, their messages are also deleted.
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )

    # Foreign key to the Conversation model, linking the message to its conversation.
    conversation = models.ForeignKey(
        'Conversation',  # Use string reference if Conversation is defined later in the same file
        # If the conversation is deleted, its messages are also deleted.
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to"
    )

    # The actual content of the message.
    message_body = models.TextField(
        help_text="The content of the message"
    )

    # Timestamp for when the message was sent.
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was sent"
    )
