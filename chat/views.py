from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Product, Message
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from products.models import Product


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

# def chat_room(request, room_name):
#     """
#     Renders the chat room interface.
#     """
#     chat_room = get_object_or_404(ChatRoom, name=room_name)
#     return render(request, 'chat/chat_room.html', {'room_name': room_name, 'chat_room': chat_room})

# @login_required
# def chat_room_list(request):
#     """
#     List all chat rooms where the user is a participant.
#     """
#     chat_rooms = ChatRoom.objects.filter(participants=request.user)
#     return render(request, 'chat/chat_room_list.html', {'chat_rooms': chat_rooms})


@login_required
def delete_message(request, message_id):
    """
    Allows the sender, the chat room creator, or an admin to delete a message.
    GET: Show a confirmation page.
    POST: Delete the message and redirect to the chat room.
    """
    message = get_object_or_404(Message, id=message_id)
    chat_room = message.chat_room
    # Only allow deletion if the user is the sender, the chat room creator, or a superuser.
    if request.user != message.sender and request.user != chat_room.created_by and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this message.")

    if request.method == "POST":
        room_name = chat_room.name
        message.delete()
        return redirect('chat:chat_room', room_name=room_name)
    
    return render(request, 'chat/confirm_delete_message.html', {'message': message})


@login_required
def chat_room_list(request):
    """
    Lists all chat rooms the user is a participant of.
    """
    chat_list = ChatRoom.objects.filter(participants=request.user)
    # Choose the first chat as the active chat for demonstration purposes,
    # or handle it via query parameters.
    active_chat = chat_list.first() if chat_list.exists() else None
    context = {
        'chat_list': chat_list,
        'active_chat': active_chat,
    }
    return render(request, 'chat/whatsapp_chat.html', context)

@login_required
def chat_room(request, room_name):
    """
    Displays a specific chat room and its messages.
    """
    active_chat = get_object_or_404(ChatRoom, name=room_name)
    product = active_chat.product
    chat_list = ChatRoom.objects.filter(participants=request.user)
    context = {
        'active_chat': active_chat,
        'chat_list': chat_list,
        'product': product,
    }
    return render(request, 'chat/whatsapp_chat.html', context)

@login_required
def start_p2p_chat(request, pk):
    """
    Starts a chat between a buyer and a farmer for a specific product.
    """
    product = get_object_or_404(Product, pk=pk)
    farmer = product.farmer  #  Get the farmer who owns the product
    buyer = request.user  #  Get the logged-in buyer

    #  Check if a chat already exists for this product
    chat = ChatRoom.objects.filter(
        participants=buyer
    ).filter(participants=farmer, is_group=False).first()

    if not chat:
        chat = ChatRoom.objects.create(
            name=f"Chat about {product.name}",
            is_group=False,
            product=product  #  Associate the chat with the product
        )
        chat.participants.add(buyer, farmer)

    return redirect('chat:chat_room', room_name=chat.name)

# @login_required
# def whatsapp_chat(request, room_name):
#     chat_room = get_object_or_404(ChatRoom, name=room_name)
#     product = chat_room.product  # Assuming the ChatRoom model has a ForeignKey to Product
#     chat_list = ChatRoom.objects.filter(participants=request.user)
#     return render(request, 'chat/whatsapp_chat.html', {
#         'active_chat': chat_room,
#         'chat_list': chat_list,
#         'product': product,
#     })
