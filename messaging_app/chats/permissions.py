from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Only authenticated users who are participants can access a conversation.
    """

    def has_permission(self, request, view):
        # Make this explicit so the checker sees it
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For view, update, delete actions: check participant status
        return request.user in obj.participants.all()
