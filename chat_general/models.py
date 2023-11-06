from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatMessageGeneral(models.Model):
    sender_general = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender_general')
    recipient_general = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver_general', default=None)
    content_general = models.TextField()
    created_at_general = models.DateTimeField(default=timezone.now)

    def get_role(self, user):
        if user == self.sender_general:
            return 'sender'
        elif user == self.recipient_general:
            return 'recipient'
        return None

    def __str__(self):
        return self.content_general