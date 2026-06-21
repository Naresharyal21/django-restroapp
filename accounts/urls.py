from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_view , name="login_url"),
    path('logout/', views.logout_view , name="logout_url"),
]
