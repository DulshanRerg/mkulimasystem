from django.shortcuts import render, get_object_or_404
from .models import ChatRoom

def chat_room(request, room_name):
    """
    Renders the chat room interface.
    """
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    return render(request, 'chat/chat_room.html', {'room_name': room_name, 'chat_room': chat_room})
