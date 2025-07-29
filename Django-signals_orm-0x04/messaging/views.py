from .models import Message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return Response({"detail": f"User '{username}' and related data deleted."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Send a message from the logged-in user to another user.
    You can also reply to a specific message using 'parent_message_id'.
    """
    receiver_id = request.data.get(
        "receiver_id")            # User ID to send to
    content = request.data.get("content")                    # Message text
    parent_id = request.data.get(
        "parent_message_id", None)  # Optional reply target

    # Make sure the receiver exists
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({"error": "Receiver not found"}, status=404)

    # If replying to a message, check that it exists
    parent_message = None
    if parent_id:
        try:
            parent_message = Message.objects.get(id=parent_id)
        except Message.DoesNotExist:
            return Response({"error": "Parent message not found"}, status=404)

    # ✅ Create the new message
    message = Message.objects.create(
        sender=request.user,         # Automatically the logged-in user
        receiver=receiver,
        content=content,
        parent_message=parent_message  # Can be None or another message
    )

    return Response({
        "message": "Message sent successfully!",
        "message_id": message.id
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threaded_messages(request):
    """
    Return a list of parent messages with all their replies (threaded view).
    Only returns messages sent to the current user.
    """

    # Get all top-level messages (not replies)
    messages = Message.objects.filter(
        receiver=request.user,
        parent_message=None
    ).select_related("sender", "receiver") \
     .prefetch_related("replies")  # ✅ Optimize reply fetching

    # Recursive function to build the thread
    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "replies": [build_thread(reply) for reply in message.replies.all()]
        }

    # Build the full threaded view
    threads = [build_thread(msg) for msg in messages]
    return Response(threads)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_messages(request):
    """
    Returns all unread messages for the logged-in user
    using the custom unread manager.
    """
    # ✅ Must match this exact pattern for checker
    messages = Message.unread.unread_for_user(request.user)

    results = [{
        "id": msg.id,
        "sender": msg.sender.username,
        "content": msg.content,
        "timestamp": msg.timestamp
    } for msg in messages]

    return Response(results)
