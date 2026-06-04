import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage, ChatRoom
from accounts.models import User
import base64


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
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
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        image_data = text_data_json.get('image')
        voice_data = text_data_json.get('voice')
        sender_id = text_data_json.get('sender_id')
        
        room = await sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        
        # Save message to database
        chat_message = await sync_to_async(ChatMessage.objects.create)(
            room=room,
            sender=sender,
            message=message if message else None,
            image=None,
            voice=None
        )
        
        # Handle image
        if image_data:
            image_bytes = base64.b64decode(image_data)
            await sync_to_async(chat_message.image.save)(f'image_{chat_message.id}.png', image_bytes, save=True)
        
        # Handle voice
        if voice_data:
            voice_bytes = base64.b64decode(voice_data)
            await sync_to_async(chat_message.voice.save)(f'voice_{chat_message.id}.webm', voice_bytes, save=True)
        
        await sync_to_async(chat_message.save)()
        
        image_url = await sync_to_async(lambda: chat_message.image.url if chat_message.image else None)()
        voice_url = await sync_to_async(lambda: chat_message.voice.url if chat_message.voice else None)()
        created_at = await sync_to_async(lambda: chat_message.created_at.strftime('%H:%M'))()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'image': image_url,
                'voice': voice_url,
                'created_at': created_at
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        image = event['image']
        voice = event['voice']
        created_at = event['created_at']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'image': image,
            'voice': voice,
            'created_at': created_at
        }))
