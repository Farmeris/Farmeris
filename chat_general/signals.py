from django.db.models.signals import post_save
from django.dispatch import receiver
from chat_general.models import ChatMessageGeneral

@receiver(post_save, sender=ChatMessage)
def create_general_chat_message(sender, instance, created, **kwargs):
    if created:
        # Create a corresponding message in the general chat
        ChatMessageGeneral.objects.create(
            sender_general=instance.recipient,
            recipient_general=instance.sender,
            content_general=''
        )