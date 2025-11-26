from rest_framework import serializers
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'
    
    def get_history(self, obj):
        # Retrieve the edit history of the current message
        history_qs = obj.history.all().order_by('-edited_at')
        return MessageHistorySerializer(history_qs, many=True).data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = '__all__'