from django.contrib import admin
from .models import ChatMessage
from chat_general.models import ChatMessageGeneral

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'polozka', 'created_at')
    list_filter = ('sender', 'recipient', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'content')

admin.site.register(ChatMessage, ChatMessageAdmin)

class ChatMessageGeneralAdmin(admin.ModelAdmin):
    list_display = ('sender_general', 'recipient_general', 'content_general', 'created_at_general')
    list_filter = ('sender_general', 'recipient_general', 'created_at_general')
    search_fields = ('sender__username', 'recipient__username', 'content')

admin.site.register(ChatMessageGeneral, ChatMessageGeneralAdmin)