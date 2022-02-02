"""
This is a synchronous WebSocket consumer that accepts all connections,
receives messages from its client, and echos those messages back to the
same client. For now it does not broadcast messages to other clients in the
same room.
"""

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import (
                                WebsocketConsumer,
                                AsyncWebsocketConsumer
                                )

# A consumer would generally inherit from one of channels base classes
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): # it would have a connect metho
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code): # and a disconnect methond, to close connections
        # Leave room group
        await self.channel_layer.discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        This method receives text data in JSON
        format and loads into a python native type(dict)
        """
        text_data_json = json.loads(text_data) # convert to dict
        message = text_data_json['message'] # grab the message sent

        # send the message back using the send method
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                })

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

"""
When a user posts a message,
a JavaScript function will transmit the message over WebSocket
to a ChatConsumer.
The ChatConsumer will receive that message and forward it to the group
corresponding to the room name. Every ChatConsumer in the same group
(and thus in the same room) will then receive the message from the group
and forward it over WebSocket back to JavaScript, where it will be appended
to the chat log.
"""
