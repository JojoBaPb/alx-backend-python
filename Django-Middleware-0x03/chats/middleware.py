import logging
from django.http import HttpResponseForbidden
from datetime import datetime
from django.http import JsonResponse

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce for authenticated users with roles
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            role = getattr(user, 'role', None)

            if role not in ['admin', 'moderator']:
                return JsonResponse(
                    {"error": "You do not have permission to perform this action."},
                    status=403
                )

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    OFFENSIVE_WORDS = ['offensive', 'badword', 'curse']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        data_sources = []

        # Collect query params
        if request.GET:
            data_sources.append(request.GET)

        # Collect POST data
        if request.method == "POST":
            data_sources.append(request.POST)

        for data in data_sources:
            for key, value in data.items():
                for word in self.OFFENSIVE_WORDS:
                    if word.lower() in value.lower():
                        return JsonResponse(
                            {"error": "Offensive language is not allowed."},
                            status=400
                        )

        return self.get_response(request)
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger(__name__)
        logger.info(f"{request.method} request to {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Allow access between 8 AM and 6 PM
        if now.hour < 8 or now.hour >= 18:
            return HttpResponseForbidden("Access is only allowed between 8 AM and 6 PM.")
        return self.get_response(request)

class AccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # List of allowed IP addresses
        self.allowed_ips = ['127.0.0.1', 'localhost']

    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)

        if ip not in self.allowed_ips:
            return HttpResponseForbidden("Access Denied")

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Handle common proxy headers
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
