from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only log if the message already exists (i.e. being updated)
    if instance.pk:
        try:
            old_msg = Message.objects.get(pk=instance.pk)
            if old_msg.content != instance.content:
                # Try to detect the user — fallback to None
                edited_by = getattr(instance, 'edited_by', None)
                # Save the old version
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_msg.content,
                    edited_by=edited_by
                )
                # Mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass
