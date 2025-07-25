# chats/permissions.py

from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only conversation participants to access messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Conversation access
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # Message access (check related conversation)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
