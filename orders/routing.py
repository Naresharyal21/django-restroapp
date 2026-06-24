from django.urls import path
from .consumers import KitchenOrderConsumer ,WaiterTableConsumer

websocket_urlpatterns = [
    path("ws/kitchen/<str:station_code>/", KitchenOrderConsumer.as_asgi()),


    path(
        "ws/waiter/tables/",
        WaiterTableConsumer.as_asgi()
    ),

]


