from django_filters import rest_framework as filters
from .models import Message, Conversation


class MessageFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender = filters.CharFilter(
        field_name='sender__username', lookup_expr='icontains')  # or use ID

    class Meta:
        model = Message
        fields = ['sender', 'start_time', 'end_time']


class ConversationFilter(filters.FilterSet):
    created_at = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Conversation
        fields = ['created_at']
