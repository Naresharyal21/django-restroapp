from django.shortcuts import render ,redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .decorators import role_required 
from accounts.models import User
from .import signals #to activate active signals
from .models import Table ,Category,Order,MenuItems,OrderItem ,KitchenStation
import json 
from django.contrib import messages
from urllib.parse import urlencode
from django.db.models import Exists,OuterRef

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse
from django.http import JsonResponse

# Create your views here.
@role_required([User.ROLE_CHOICES.WAITER])
def table_views(request):
  tables=Table.objects.all()

  return render(request ,'orders/tables.html',{
    'tables':tables
  })


@role_required([User.ROLE_CHOICES.WAITER])
def menu_views(request , table_id):
   table = Table.objects.get(id=table_id)

   if request.method=="POST":
    data=request.POST.get("order-items")

    if not data:
            messages.error(request, "No items selected")
            return redirect("table_view_url")
    data_dict=json.loads(data)
   
    table_id=data_dict.get('table_id')
    table_obj=Table.objects.get(pk=table_id)
    order=Order.objects.create(table=table)

    for orderitem in data_dict.get("items",[]):
      menu_item=MenuItems.objects.get(pk=orderitem.get("item_id"))
      order_item=OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        price=menu_item.price,
        quantity=orderitem.get("quantity"),
        priority=menu_item.default_priority
      )

      station_code = order_item.menu_item.station.code
      channel_layer = get_channel_layer()
      async_to_sync(channel_layer.group_send)(
    f"kitchen_{station_code}",
    {
        "type": "new_order",
        "order": {
            "item_name": str(order_item),
            "priority": order_item.priority,
            "priority_display": order_item.get_priority_display(),
        }
    }
)
      
      messages.success(request,"order created sucess")
   
    return redirect("table_view_url")

   table=Table.objects.get(id=table_id)
   categories=Category.objects.all()
   orders=Order.objects.filter(table_id=table_id).exclude(status=Order.ORDER_STATUS.BILLED).order_by("-created_at")

 
   return render(request ,'orders/menu.html',{
    'categories':categories,
    'table':table,
    'orders':orders,
  })

@role_required([User.ROLE_CHOICES.KITCHEN])
def kitchen_dashboard_view(request):
    station_code=request.GET.get('station_code')

    if station_code is not None:
        orderitems=OrderItem.objects.filter(menu_item__station__code=station_code)
    else:
        
    
    # stations = KitchenStation.objects.all()
    # print(stations),
     orderitems = OrderItem.objects.all().order_by("-priority")
    grouped_items = {}
    
    for item in orderitems:
        station_name = item.menu_item.station.name
        if station_name not in grouped_items.keys():
            grouped_items[station_name] = [item]
        else:
            grouped_items[station_name].append(item)
            
    # print(grouped_items)
    
    return render(request, "orders/kitchen_dashboard.html", {
        # 'stations': stations
        'order_items': grouped_items
    })

@role_required([User.ROLE_CHOICES.KITCHEN])
def kitchen_station_dashboard_view(request):

    orderitems = OrderItem.objects.filter(
        menu_item__station__code=request.user.kitchen_station
    ).order_by("-priority")

    return render(request, "orders/station_dashboard.html", {
        "order_items": orderitems,
        "station": request.user.kitchen_station,
        "station_name": request.user.get_kitchen_station_display(),
    })


   


@role_required([User.ROLE_CHOICES.KITCHEN])
def mark_item_ready(request, item_id):
    order_item = OrderItem.objects.get(id=item_id)

    order_item.status = OrderItem.ITEM_STATUS.READY
    order_item.save()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "waiter_tables",
        {
            "type": "table_ready",
            "table_id": order_item.order.table.id,
        }
    )

    return redirect("kitchen_dashboard_station_view_url")

@role_required([User.ROLE_CHOICES.WAITER])
def served_conformation(request,order_item_id):
   
   if item_id is not None:
      order_item=get_object_or_404(OrderItem,pk=order_item_id)
      order_item.status=OrderItem.ITEM_STATUS.SERVED
      order_item.save()
      return redirect("menu_view_url") 
   "order_item"=order_item