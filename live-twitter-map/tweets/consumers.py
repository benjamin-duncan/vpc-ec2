import os
import json
from channels.generic.websocket import AsyncWebsocketConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from tweets.redis import redis
from django.conf import settings
import uuid
class TweetsConsumer(AsyncWebsocketConsumer):
    GROUP = 'tweet'
    flag = 1
    async def connect(self):

        self.flag = uuid.uuid4().hex
        redis.set(f'filter {self.flag}',"")
        if False: #self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.GROUP,
                self.channel_name
            )
            await self.accept()

    # SOMETHING FROM CLIENT DO STUFF
    # REDIS.SET(FILTER PARAMS)
    # login with auth to twitter 
    # filter only tweets that the account follows

    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        redis.set(f'filter {self.flag}',message)
        
        await self.channel_layer.group_send(
            self.GROUP,
            {
                'type': 'text_message',
                'message': message
            }
        )

    async def text_message(self, event):
        if True: #not self.scope["user"].is_anonymous:
            message =event['message']

            
            # IF MESSAGE TEXT CONTAINS REDIS.GET FILTEREED SUTFF THEN SEND TO CLIENT
            filter = redis.get(f"filter {self.flag}")
            
            if filter in message:
                await self.send(text_data=json.dumps({
                    'message': message
                }))