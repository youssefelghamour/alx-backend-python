from datetime import datetime
import logging


logger = logging.getLogger(__name__)
if not logger.handlers:
    fh = logging.FileHandler('requests.log')
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """A middleware that logs each user’s requests to a file, including:
        - The timestamp
        - The user
        - The request path
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response