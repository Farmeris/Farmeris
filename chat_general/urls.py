from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from search import views as search_views
from chat_general import views as chat_general_views


app_name = 'chat_general'

urlpatterns = [
    # Redirect URL pattern
    path('<str:username>/chats/<str:sender>/', chat_general_views.redirect_to_chat_general, name='redirect_to_chat_general'),

    path('<str:username>/chats/', chat_general_views.chat_general, name='user_chat_general'),
    path('<str:username>/chats/<str:sender>/', chat_general_views.chat_general, name='user_chat_general_with_sender'),
    path('<str:username>/chats/<str:sender>/send_message', chat_general_views.send_message_in_general_chat, name='send_message_in_general_chat'),

    path('<str:username>/chats_mobile/', chat_general_views.chat_general_mobile, name='chat_general_mobile'),
    path('<str:username>/chats_mobile/<str:sender>/', chat_general_views.chat_general_mobile, name='chat_general_mobile_with_sender'),
] 