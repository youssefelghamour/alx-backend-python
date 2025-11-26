from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Signal to send a notification when a new message is sent"""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def save_message_edit_history(sender, instance, **kwargs):
    """Signal to save message edit history when a message is being edited"""
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # If the message does not exist, it's a new message
        # Which means this is not an edit, it's a creation
        return
    
    if old_message.content != instance.content:
        # Content has changed, save the old content to MessageHistory
        MessageHistory.objects.create(
            message=old_message,
            edited_by=old_message.sender,
            old_content=old_message.content
        )
        instance.edited = True  # Mark the message as edited