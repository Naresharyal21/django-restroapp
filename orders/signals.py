# from .models import Order
# from django.dispatch import receiver
# from  django.db.models.signals import pre_save , post_save




# @receiver(pre_save, sender=Order)
# def handle_order_pre_save(sender , **kwargs):














# #friday
# @receiver(post_save,sender=OrderItem)
# def handke_auto_order_status_update(sender, **kwargs):
#   order_item=kwargs.get('instance')

#   if order_item.status== OrderItem.ITEM_STATUS>SERVED:
#     print(OrderItem)