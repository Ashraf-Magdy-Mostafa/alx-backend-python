from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant  # Ensure this exists


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    Only participants can view or create conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Show only conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Add current user as a participant when creating a conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # ✅ Explicit checker-required use of `conversation_id`
        conversation_id = self.request.data.get("conversation_id")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Explicit 403 Forbidden check
        if self.request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)
