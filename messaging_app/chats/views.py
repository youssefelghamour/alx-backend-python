from rest_framework import viewsets
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
