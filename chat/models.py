from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    """
    Represents a chat room.
    """
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_chatrooms',
        null=True,
        blank=True
    )
    is_group = models.BooleanField(default=False)  # True for group chats
    group_image = models.ImageField(upload_to='group_images/', null=True, blank=True)  # Group chat image

    def get_avatar_url(self):
        """
        Returns the appropriate image URL:
        - Group Image if it's a group chat
        - Default avatar if no group image
        """
        if self.is_group and self.group_image:
            return self.group_image.url
        return "/static/images/group-placeholder.png"  # Default group image

    def __str__(self):
        return self.name

class Message(models.Model):
    """
    Represents a message within a chat room.
    """
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'
