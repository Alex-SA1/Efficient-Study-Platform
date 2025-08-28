import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import StudySessionMessage
from asgiref.sync import sync_to_async
from .utils import remove_user_from_study_session, study_session_empty, remove_study_session
from django.utils import timezone
from datetime import datetime as datetimeClass


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tzname = self.scope['session'].get('django_timezone')
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
        profile_picture_url = text_data_json["profile_picture_url"]

        await self.save_message(message)

        sender = self.user.username
        datetime = timezone.now().isoformat()

        await self.channel_layer.group_send(
            self.session_group_name, {
                "type": "chat.message", "message": message, "sender": sender, "datetime": datetime, "profile_picture_url": profile_picture_url}
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        received_datetime = event["datetime"]
        profile_picture_url = event["profile_picture_url"]

        await sync_to_async(timezone.activate)(self.tzname)

        received_datetime = datetimeClass.fromisoformat(received_datetime)

        datetime = timezone.localtime(received_datetime).isoformat()

        await self.send(text_data=json.dumps({"message": message, "sender": sender, "datetime": datetime, "profile_picture_url": profile_picture_url}))
