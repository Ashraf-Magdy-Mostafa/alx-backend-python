from jwt import decode, InvalidTokenError
from django.conf import settings
from django.contrib.auth import get_user_model
from uuid import UUID
import logging
from datetime import datetime
from django.http import HttpResponseForbidden

User = get_user_model()


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = "Anonymous"
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:

                payload = decode(token, settings.SECRET_KEY,
                                 algorithms=["HS256"])
                user_id_str = payload.get("user_id")
                if user_id_str:
                    try:
                        user_uuid = UUID(user_id_str)
                        user_obj = User.objects.get(
                            user_id=user_uuid)
                        user = user_obj.username
                    except (User.DoesNotExist, ValueError):
                        user = "UnknownUser"
            except InvalidTokenError:
                user = "InvalidToken"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        return self.get_response(request)


# Restrict access from 6 to 9 pm


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        # Define allowed time window: 18:00 to 21:00
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Chat is only accessible between 6 PM and 9 PM.")

        return self.get_response(request)
