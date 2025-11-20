from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAuthenticatedUser, IsParticipantOfConversation


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]  


class ConversationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        """Only show conversations the logged in user is part of"""
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsParticipantOfConversation]
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        """Show messages for a specific conversation only if the logged in user is a participant"""

        # Only show messages for this conversation: api/conversations/{conversation_pk}/messages/
        conversation_id = self.kwargs['conversation_pk']
        conversation = Conversation.objects.get(conversation_id=conversation_id)

        # Check that the logged-in user is a participant
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not part of this conversation.", code=status.HTTP_403_FORBIDDEN)

        # Return all messages in this conversation from all participants
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        """Only a logged in user who is part of the conversation can send a message"""

        # Get conversation from URL and user from request
        conversation = Conversation.objects.get(pk=self.kwargs['conversation_pk'])

        # Get the user from request.user & Ensure the sender is part of the conversation
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation.")

        serializer.save(
            conversation=conversation,
            sender=self.request.user
        )
