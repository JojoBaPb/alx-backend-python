import logging
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger(__name__)
        logger.info(f"{request.method} request to {request.path}")
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
