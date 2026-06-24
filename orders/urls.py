from django.contrib import admin
from django.urls import path
from  .import views
from .consumers import KitchenOrderConsumer

urlpatterns = [
    path('tables/', views.table_views , name="table_view_url"),

    path('menu/<table_id>/', views.menu_views , name="menu_view_url"),

     path("kitchen/dashboard/", views.kitchen_dashboard_view, 
     name="kitchen_dashboard_view_url"),


     path("kitchen/dashboard/station/", views.kitchen_station_dashboard_view, name="kitchen_dashboard_station_view_url"),

#  path("kitchen/<station_code>/live/", views.kitchen_dashboard_live_view, name="kitchen_dashboard_view_live_url"),
     
     path(
    "kitchen/item/<int:item_id>/ready/",
    views.mark_item_ready,
    name="mark_item_ready_url"
),

 ]



  