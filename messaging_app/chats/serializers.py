from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'role']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model"""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        required=True
    )
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def validate_participant_ids(self, value):
        """Ensure at least two participants are included in the conversation"""
        if len(value) < 2:
            raise serializers.ValidationError("Conversation must have at least 2 participants.")
        return value

    def create(self, validated_data):
        """Create Conversation with participants"""
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        return conversation
    
    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def validate_sender(self, value):
        """Ensure sender is provided"""
        if not value:
            raise serializers.ValidationError("Sender must be provided.")
        return value