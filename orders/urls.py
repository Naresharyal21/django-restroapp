from django.contrib import admin
from django.urls import path
from orders import views

urlpatterns = [
    path('tables/', views.table_views , name="table_view_url"),
    path('menu/<table_id>/', views.menu_views , name="menu_view_url"),
#     path('menu/')
 ]
