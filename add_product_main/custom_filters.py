from django import template

register = template.Library()

@register.filter
def unique_senders(chat_messages):
    user_set = set()
    unique_messages = []
    for message in chat_messages:
        if message.sender != message.request.user and message.sender not in user_set:
            unique_messages.append(message)
            user_set.add(message.sender)
    return unique_messages