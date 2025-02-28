from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom
from django.db import IntegrityError

@login_required
def create_chat_room(request):
    """
    View to create a new chat room.
    If a chat room with the given name exists, it returns that room.
    Otherwise, it creates a new one.
    """
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            try:
                # This will either get the existing chat room or create a new one.
                chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
                # Add the user as a participant if they're not already in it.
                chat_room.participants.add(request.user)
                return redirect('chat:chat_room', room_name=room_name)
            except IntegrityError:
                # Handle the case where the chat room already exists
                chat_room = ChatRoom.objects.get(name=room_name)
                chat_room.participants.add(request.user)
                return redirect('chat:chat_room', room_name=room_name)
    return render(request, 'chat/create_chat_room.html')

def chat_room(request, room_name):
    """
    Renders the chat room interface.
    """
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    return render(request, 'chat/chat_room.html', {'room_name': room_name, 'chat_room': chat_room})

@login_required
def chat_room_list(request):
    """
    List all chat rooms where the user is a participant.
    """
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chat/chat_room_list.html', {'chat_rooms': chat_rooms})