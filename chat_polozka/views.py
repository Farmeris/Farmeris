from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from add_product_main.models import Polozka
from chat_polozka.models import ChatMessage
from django.core.exceptions import PermissionDenied
from django.urls import reverse

@login_required
def chat(request, username, nazov_produktu):
    # Retrieve the polozka object
    #polozka = Polozka.objects.get(user_profile__user__username=username, nazov_produktu=nazov_produktu)#toto fungovalo, druha moznost je vraj lepsia
    #recipient = User.objects.get(username=username)
    polozka = get_object_or_404(Polozka, user_profile__user__username=username, nazov_produktu=nazov_produktu)
    recipient = User.objects.get(user_profile__user__username=username)

    if request.user == polozka.user_profile.user:
        raise PermissionDenied

    context = {
        'username': username,
        'polozka': polozka,
        'recipient': recipient,
    }
    
    return render(request, 'chat_polozka/chat_polozka_zobrazenie.html', context)

@login_required
def send_message_in_polozka(request, username, nazov_produktu):
    if request.method == 'POST':
        message_content = request.POST['message'].strip()
        if message_content:  # Check if the message content is not empty
            polozka = get_object_or_404(Polozka, user_profile__user__username=username, nazov_produktu=nazov_produktu)

            #if request.user == polozka.user_profile.user:
            #    raise PermissionDenied

            recipient = get_object_or_404(User, username=username)

            message = ChatMessage.objects.create(
                sender=request.user,
                recipient=recipient,
                content=message_content,
                polozka=polozka
            )
    # Get the ID of the last message
    last_message_id = ChatMessage.objects.latest('created_at').id
    
    redirect_url = reverse('add_product_main:user_zobraz_polozku', kwargs={
        'username': username,
        'nazov_produktu': nazov_produktu,
        'anchor': last_message_id  # Pass the ID as an anchor
    })
    
    return redirect(redirect_url)

    #chat_messages = polozka.chat_messages.order_by('created_at')

    #return redirect('add_product_main:user_zobraz_polozku', username=username, nazov_produktu=nazov_produktu)