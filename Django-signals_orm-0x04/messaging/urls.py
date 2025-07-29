from .views import send_message, threaded_messages
from django.urls import path

urlpatterns = [
    path('send-message/', send_message),
    path('threaded-messages/', threaded_messages),
]
