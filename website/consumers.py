import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import StudySessionMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.session_code = self.scope["url_route"]["kwargs"]["session_code"]
        self.session_group_name = f"study_session_{self.session_code}"

        await self.channel_layer.group_add(self.session_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.session_group_name, self.channel_name)

    async def save_message(self, message):
        await database_sync_to_async(StudySessionMessage.objects.create)(
            user=self.user,
            group_name=self.session_group_name,
            message_content=message
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.session_group_name, {
                "type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
