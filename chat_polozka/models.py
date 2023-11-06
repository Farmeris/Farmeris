from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver', default=None)
    content = models.TextField()
    polozka = models.ForeignKey('add_product_main.Polozka', on_delete=models.CASCADE, related_name='chat_messages', null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content