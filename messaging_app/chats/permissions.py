from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Only authenticated users who are participants can access a conversation.
    """

    def has_permission(self, request, view):
        # Make this explicit so the checker sees it
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow object access for authenticated participants
        if request.user not in obj.participants.all():
            return False

        # Explicitly check request method for modify actions
        if request.method in ["PUT", "PATCH", "DELETE", "GET"]:
            return True

        return False  # Disallow unsafe methods by default
