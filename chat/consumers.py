import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """
        Handles receiving a new message from WebSocket and saves it.
        """
        data = json.loads(text_data)
        message_content = data['message']
        sender = self.scope["user"]  # Get the authenticated user

        # Ensure the room exists
        chat_room = ChatRoom.objects.get(name=self.room_name)

        # Save message to database
        new_message = Message.objects.create(
            chat_room=chat_room,
            sender=sender,
            content=message_content
        )

        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_content,
                "sender": sender.username,
                "timestamp": new_message.timestamp.strftime('%H:%M')
            }
        )

    def chat_message(self, event):
        """
        Sends messages to WebSocket clients.
        """
        self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"]
        }))
