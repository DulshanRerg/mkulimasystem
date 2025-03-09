# chat/urls.py
from django.urls import path
from .views import create_chat_room, chat_room, chat_room_list, delete_message, start_p2p_chat

app_name = 'chat'

urlpatterns = [
    path('create/', create_chat_room, name='create_chat_room'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
    path('rooms/', chat_room_list, name='chat_room_list'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('start_p2p_chat/<int:pk>/', start_p2p_chat, name='start_p2p_chat'),
]
