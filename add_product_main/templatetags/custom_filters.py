from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter
def decimal_places(value, places):
    try:
        decimal_value = Decimal(value)
        formatted_value = '{:.{}f}'.format(decimal_value, places).rstrip('0').rstrip('.')
        return formatted_value
    except (InvalidOperation, TypeError, ValueError):
        return value

@register.filter
def unique_senders(chat_messages):
    user_set = set()
    unique_messages = []
    for message in chat_messages:
        if message.sender not in user_set:
            unique_messages.append(message)
            user_set.add(message.sender)
    return unique_messages