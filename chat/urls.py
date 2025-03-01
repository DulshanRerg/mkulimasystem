# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room/<str:room_name>/', views.chat_room, name='chat_room'),
    path('create/', views.create_chat_room, name='create_chat_room'),
    path('my-rooms/', views.chat_room_list, name='chat_room_list'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
