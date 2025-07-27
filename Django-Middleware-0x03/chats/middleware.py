import logging

logger = logging.getLogger(__name__)

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the method and path of every incoming request
        logger.info(f"{request.method} request to {request.path}")

        response = self.get_response(request)
        return response

