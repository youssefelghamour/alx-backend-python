from rest_framework import viewsets, status, filters  # <- both imported
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]  

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        # Only show messages for this conversation
        return Message.objects.filter(conversation_id=self.kwargs['conversation_pk'])

    def perform_create(self, serializer):
        # Get conversation from URL
        conversation = Conversation.objects.get(pk=self.kwargs['conversation_pk'])
        serializer.save(conversation=conversation)
