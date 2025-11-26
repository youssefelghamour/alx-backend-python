from rest_framework import viewsets
from .models import Message, Notification, MessageHistory
from .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer, ThreadMessageSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """ The sender of a reply is the logged-in user sending it: sender = request.user
            The receiver of a reply is the other participant in the parent message

            Example: Conversation between A and B:
                - Message 1: A sends to B
                    - If A replies to this message -> it goes to B
                    - If B replies to this message -> it goes to A
                - Message 2: B sends to A
                    - If B replies to this message -> it goes to A
                    - If A replies to this message -> it goes to B
            
            Maintains a conversation between two users
        """
        parent_message = serializer.validated_data.get('parent_message')
        if parent_message:  # if it's a reply
            # User replies to their own message in a conversation (A replies to 1)
            if self.request.user == parent_message.sender:
                serializer.save(sender=self.request.user, receiver=parent_message.receiver)
            # User replies to the other user's message (B replies to 1)
            elif self.request.user == parent_message.receiver:
                serializer.save(sender=self.request.user, receiver=parent_message.sender)
        else:
            # normal message
            serializer.save(sender=self.request.user)


class ThreadsViewSet(viewsets.ViewSet):
    """ Returns all top-level messages (messages with no parent) and their full reply trees
        Replies are prefetched to avoid extra database queries
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        top_messages = Message.objects.filter(parent_message__isnull=True)\
            .select_related('sender', 'receiver')\
            .prefetch_related(
                'replies__sender',
                'replies__receiver',
                'replies__replies__sender',
                'replies__replies__receiver'
            )

        serializer = ThreadMessageSerializer(top_messages, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """A view that deletes the currently logged-in user"""
    user = request.user
    user.delete()
    return Response({'status': 'User deleted'})


class MessageHistoryViewSet(viewsets.ModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer