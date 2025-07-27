class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"{request.method} request to {request.path}")
        return self.get_response(request)

