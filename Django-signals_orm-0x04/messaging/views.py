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
