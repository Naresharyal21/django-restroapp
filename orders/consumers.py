import json
from channels.generic.websocket import AsyncWebsocketConsumer


class KitchenOrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.station_code = self.scope["url_route"]["kwargs"]["station_code"]
        self.group_name = f"kitchen_{self.station_code}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def new_order(self, event):
        await self.send(text_data=json.dumps(event["order"]))


        import json
from channels.generic.websocket import AsyncWebsocketConsumer


class WaiterTableConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            "waiter_tables",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "waiter_tables",
            self.channel_name
        )

    async def table_ready(self, event):
        await self.send(
            text_data=json.dumps({
                "table_id": event["table_id"]
            })
        )