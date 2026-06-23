from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):

    class ROLE_CHOICES(models.TextChoices):
        WAITER = "w", "Waiter"
        BILLING = "b", "Billing"
        KITCHEN = "k", "Kitchen"
        OWNER = "o", "Owner"

    class KITCHEN_STATION_CHOICES(models.TextChoices):
        STEAM = "steam", "Steam Station"
        GRILL = "grill", "Grill Station"
        MAIN_KITCHEN = "main_kitchen", "Main Kitchen"
        BREAKFAST = "breakfast", "Breakfast Station"
        BEVERAGE = "beverage", "Beverage Station"
        DESSERT = "dessert", "Dessert Station"

    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES.WAITER
    )

    kitchen_station = models.CharField(
        max_length=20,
        choices=KITCHEN_STATION_CHOICES,
        blank=True,
        null=True
    )
    def clean(self):
        super().clean()

        if self.role == self.ROLE_CHOICES.KITCHEN:
            if not self.kitchen_station:
                raise ValidationError({
                    "kitchen_station": "Kitchen station is required for kitchen staff."
                })
        else:
            if self.kitchen_station:
                raise ValidationError({
                    "kitchen_station": "Only kitchen staff can have kitchen station."
                })

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    