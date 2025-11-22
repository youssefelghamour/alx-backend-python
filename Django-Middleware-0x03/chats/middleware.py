from datetime import datetime
import logging
from django.http import HttpResponseForbidden


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


class RestrictAccessByTimeMiddleware:
    """A middleware that restricts access to the site during certain hours
       For example, block access outside of 9 AM to 5 PM
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_hour = datetime.now().hour

        if current_hour < 9 or current_hour >= 17:
            return HttpResponseForbidden("Access to this site is restricted to business hours (9 AM to 5 PM).")
        
        response = self.get_response(request)
        return response