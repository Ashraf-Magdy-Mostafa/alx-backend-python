# chats/urls.py

from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
# ✅ Include UserViewSet
from .views import ConversationViewSet, MessageViewSet, UserViewSet

# Root router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # ✅ Add user viewset
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages inside conversations
conversations_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation'
)
conversations_router.register(
    r'messages', MessageViewSet, basename='conversation-messages'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
