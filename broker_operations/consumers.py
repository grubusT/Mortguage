import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Application, Task, Reminder

class BrokerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        self.user = self.scope["user"]
        self.room_group_name = f"broker_{self.user.id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'subscribe':
            # Handle subscription to specific updates
            await self.handle_subscription(text_data_json)
        elif message_type == 'unsubscribe':
            # Handle unsubscription from specific updates
            await self.handle_unsubscription(text_data_json)

    async def handle_subscription(self, data):
        subscription_type = data.get('subscription_type')
        if subscription_type in ['applications', 'tasks', 'reminders']:
            await self.channel_layer.group_add(
                f"{self.room_group_name}_{subscription_type}",
                self.channel_name
            )

    async def handle_unsubscription(self, data):
        subscription_type = data.get('subscription_type')
        if subscription_type in ['applications', 'tasks', 'reminders']:
            await self.channel_layer.group_discard(
                f"{self.room_group_name}_{subscription_type}",
                self.channel_name
            )

    async def application_update(self, event):
        # Send application update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'application_update',
            'data': event['data']
        }))

    async def task_update(self, event):
        # Send task update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'task_update',
            'data': event['data']
        }))

    async def reminder_update(self, event):
        # Send reminder update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'reminder_update',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_user_applications(self):
        return list(Application.objects.filter(broker=self.user).values())

    @database_sync_to_async
    def get_user_tasks(self):
        return list(Task.objects.filter(broker=self.user).values())

    @database_sync_to_async
    def get_user_reminders(self):
        return list(Reminder.objects.filter(broker=self.user).values()) 