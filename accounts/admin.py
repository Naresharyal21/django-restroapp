from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'username',
        'email',
        'role',
        'kitchen_station',
        'is_staff',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {
            'fields': ('role', 'kitchen_station'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {
            'fields': ('role', 'kitchen_station'),
        }),
    )