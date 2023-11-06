from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse
from django.urls import reverse
from login_app.models import UserProfile  
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from user_profile.forms import UserProfileForm
from add_product_main.models import Polozka
from urllib.parse import urlencode
from itertools import chain
from datetime import datetime
from django.db.models import Q
from django.http import QueryDict
from chat_polozka.models import ChatMessage
from chat_general.models import ChatMessageGeneral
from django.contrib.auth.decorators import login_required
import pytz

@login_required(login_url='user_profile:user_profile')
def chat_general(request, username, sender=None):

    if request.user.username != username:
        return HttpResponseForbidden()

    #user_profile = UserProfile.objects.get(user__username=username)
    query = request.GET.get('query')
    recipient = None

    if query:
        try:
            recipient = User.objects.get(username=query)
        except User.DoesNotExist:
            pass

    user_profile = UserProfile.objects.get(user=request.user)

    chat_messages_general = ChatMessageGeneral.objects.filter(
        Q(sender_general=request.user, recipient_general=recipient) |
        Q(sender_general=recipient, recipient_general=request.user)
    )

    chat_messages = ChatMessage.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user)
    )

    #all_messages = list(chat_messages) + list(chat_messages_general)
    #all_messages.sort(key=lambda x: x.timestamp)
    all_messages = [{"type": "general", "message": msg} for msg in chat_messages_general] + [{"type": "chat", "message": msg} for msg in chat_messages]

    received_senders = ChatMessageGeneral.objects.filter(
        recipient_general=request.user
    ).values_list('sender_general__username', flat=True).distinct()
    
    sent_to_senders = ChatMessageGeneral.objects.filter(
        sender_general=request.user
    ).values_list('recipient_general__username', flat=True).distinct()
    senders = list(set(received_senders) | set(sent_to_senders))

    received_from = ChatMessage.objects.filter(recipient=request.user).values_list('sender__username', flat=True).distinct()
    sent_to = ChatMessage.objects.filter(sender=request.user).values_list('recipient__username', flat=True).distinct()
    unique_chat_partners = list(set(received_from) | set(sent_to))

    combined_senders = list(set(senders) | set(unique_chat_partners))


    context = {
        'user_profile': user_profile,
        'chat_messages_general': chat_messages_general,
        'chat_messages': chat_messages,
        'query': query,
        'recipient': recipient,
        'username': username,
        'combined_senders': combined_senders,
        'all_messages': all_messages,
    }

    return render(request, 'general_chat.html', context)

@login_required(login_url='user_profile:user_profile')
def send_message_in_general_chat(request, username, sender):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        sender_general = get_object_or_404(User, username=username)
        recipient_general = get_object_or_404(User, username=sender)
        ChatMessageGeneral.objects.create(
            sender_general=sender_general,
            recipient_general=recipient_general,
            content_general=message_content
        )

        redirect_url = reverse('chat_general:user_chat_general_with_sender', kwargs={
            'username': username,
            'sender': sender,
        })
        #query_string = urlencode({'query': sender})
        #redirect_url += f'{query_string}'

        return redirect(redirect_url)
    else:
        raise Http404('Invalid request method.')

def redirect_to_chat_general(request, username, sender):
    redirect_url = f"/{username}/chats/?query={sender}"
    return redirect(redirect_url)


#mobile chat
@login_required(login_url='user_profile:user_profile')
def chat_general_mobile(request, username, sender=None):
    if request.user.username != username:
        return HttpResponseForbidden()

    #user_profile = UserProfile.objects.get(user__username=username)
    query = request.GET.get('query')
    recipient = None

    if query:
        try:
            recipient = User.objects.get(username=query)
        except User.DoesNotExist:
            pass

    user_profile = UserProfile.objects.get(user=request.user)

    chat_messages_general = ChatMessageGeneral.objects.filter(
        Q(sender_general=request.user, recipient_general=recipient) |
        Q(sender_general=recipient, recipient_general=request.user)
    )

    chat_messages = ChatMessage.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user)
    )

    received_senders = ChatMessageGeneral.objects.filter(
        recipient_general=request.user
    ).values_list('sender_general__username', flat=True).distinct()
    
    sent_to_senders = ChatMessageGeneral.objects.filter(
        sender_general=request.user
    ).values_list('recipient_general__username', flat=True).distinct()
    senders = list(set(received_senders) | set(sent_to_senders))

    received_from = ChatMessage.objects.filter(recipient=request.user).values_list('sender__username', flat=True).distinct()
    sent_to = ChatMessage.objects.filter(sender=request.user).values_list('recipient__username', flat=True).distinct()
    unique_chat_partners = list(set(received_from) | set(sent_to))

    combined_senders = list(set(senders) | set(unique_chat_partners))
    context = {
        'user_profile': user_profile,
        'chat_messages_general': chat_messages_general,
        'chat_messages': chat_messages,
        'query': query,
        'recipient': recipient,
        'username': username,
        'combined_senders': combined_senders,
    }
    
    return render(request, 'general_chat_mobile.html', context)