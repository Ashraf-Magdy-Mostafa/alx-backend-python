import time
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


# This dictionary keeps track of requests from each IP address
message_counter = {}


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check POST requests (usually used to send messages)
        if request.method == "POST":
            ip_address = self.get_client_ip(request)
            current_time = time.time()  # Get current time in seconds

            # Get the list of timestamps for this IP (or empty list if not found)
            request_times = message_counter.get(ip_address, [])

            # Keep only the timestamps from the last 60 seconds (1 minute)
            request_times = [t for t in request_times if current_time - t < 60]

            # Check if the user sent more than 5 messages in the last minute
            if len(request_times) >= 5:
                return HttpResponseForbidden("❌ Too many messages! Try again in a minute.")

            # Add this request's timestamp to the list
            request_times.append(current_time)

            # Save the updated list back to the dictionary
            message_counter[ip_address] = request_times

        # Continue to the next middleware or view
        return self.get_response(request)

    def get_client_ip(self, request):
        # Check if there's a proxy or load balancer
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Use the first IP in the list
            return x_forwarded_for.split(',')[0].strip()
        # Else, use the normal IP address
        return request.META.get('REMOTE_ADDR', '')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in
        if request.user.is_authenticated:
            # Get user role (you may use user.role or user.groups or custom logic)
            user = request.user
            # assumes you have a 'role' field
            user_role = getattr(user, "role", None)

            # Allow only if role is 'admin' or 'moderator'
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied. Only admins or moderators are allowed.")
        else:
            # If not logged in, deny access
            return HttpResponseForbidden("Authentication required.")

        # Allow the request to continue
        return self.get_response(request)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Block if not logged in
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")

        # Check if user is in 'admin' or 'moderator' group
        if not request.user.groups.filter(name__in=['admin', 'moderator']).exists():
            return HttpResponseForbidden("Only admins or moderators can access this.")

        return self.get_response(request)
