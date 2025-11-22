from datetime import datetime


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
        with open('requests.log', 'a') as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path} \n")

        response = self.get_response(request)
        return response