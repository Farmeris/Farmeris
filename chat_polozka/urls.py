from django.urls import path
from . import views

app_name = 'chat_polozka'

urlpatterns = [
    path('<str:username>/polozka/<str:nazov_produktu>/chat/', views.chat, name='chat'),
    path('<str:username>/polozka/<str:nazov_produktu>/send_message/', views.send_message_in_polozka, name='send_message_in_polozka'),
]
