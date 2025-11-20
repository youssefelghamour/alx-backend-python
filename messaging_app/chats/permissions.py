from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedUser(IsAuthenticated):
    """ Allows access only to authenticated users
        Uses Django REST Framework's built-in IsAuthenticated permission

        Not overriding it, it still behaves exactly like IsAuthenticated
    """
    pass
