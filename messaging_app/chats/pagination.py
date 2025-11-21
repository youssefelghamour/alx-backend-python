from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """Pagination class for messages in a conversation: 20 messages per page"""
    page_size = 20  # Number of messages per page