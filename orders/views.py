from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .decorators import role_required
from accounts.models import User
from .import signals #to activate active signals
from .models import Table ,Category,Order,MenuItems,OrderItem
import json
from django.contrib import messages

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
      OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        price=menu_item.price,
        quantity=orderitem.get("quantity")
      )
      
      messages.success(request,"order created sucess")
   
    return redirect("table_view_url")

   table=Table.objects.get(id=table_id)
   categories=Category.objects.all()
 
   return render(request ,'orders/menu.html',{
    'categories':categories,
    'table':table,
  })




#code to prepration history order