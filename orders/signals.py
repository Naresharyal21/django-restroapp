from .models import Order, OrderHistory, OrderItem
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=OrderItem)
def handle_auto_order_status_update(sender, instance, **kwargs):
    order_item = instance

    if order_item.status == OrderItem.ITEM_STATUS.READY:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "waiter_tables",
            {
                "type": "table_ready",
                "table_id": order_item.order.table.id,
            }
        )

    if order_item.status == OrderItem.ITEM_STATUS.SERVED:
        all_items = OrderItem.objects.filter(order=order_item.order)

        for item in all_items:
            if item.status != OrderItem.ITEM_STATUS.SERVED:
                order_item.order.status = Order.ORDER_STATUS.PARTIALLY_SERVED
                order_item.order.save()
                break
        else:
            order_item.order.status = Order.ORDER_STATUS.SERVED
            order_item.order.save()