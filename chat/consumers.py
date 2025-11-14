import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message
from .encryption import encrypt_message, decrypt_message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope.get('user')
        
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        
        has_access = await self.check_room_access()
        if not has_access:
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        encrypted_message = encrypt_message(message)
        
        await self.save_message(encrypted_message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
    
    @database_sync_to_async
    def check_room_access(self):
        try:
            room = Room.objects.get(id=self.room_id)
            session = self.scope.get('session', {})
            return session.get(f'room_{self.room_id}_access', False)
        except Room.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, encrypted_message):
        room = Room.objects.get(id=self.room_id)
        Message.objects.create(
            room=room,
            sender=self.user,
            encrypted_content=encrypted_message
        )
