from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import pre_save

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification when a new message is created
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    try:
        original = Message.objects.get(id=instance.id)
        if original.content != instance.content:  # If the content has changed
            # Save the old content before updating
            MessageHistory.objects.create(message=instance, old_content=original.content)
            instance.edited = True  # Mark the message as edited
    except Message.DoesNotExist:
        pass  # No original message, likely a new message

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
