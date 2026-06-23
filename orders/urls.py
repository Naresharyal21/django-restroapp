from django.contrib import admin
from django.urls import path
from  .import views

urlpatterns = [
    path('tables/', views.table_views , name="table_view_url"),

    path('menu/<table_id>/', views.menu_views , name="menu_view_url"),

     path("kitchen/dashboard/", views.kitchen_dashboard_view, 
     name="kitchen_dashboard_view_url"),


     path("kitchen/dashboard/station/", views.kitchen_station_dashboard_view, name="kitchen_dashboard_station_view_url"),
     

 ]



  