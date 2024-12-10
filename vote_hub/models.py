from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(null=False, blank=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["name", "location"], name="unique_restaurant")
        ]


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="restaurant"
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["restaurant", "date"], name="unique_menu_per_day")
        ]

    def __str__(self):
        return f"Menu for restaurant {self.restaurant.name} on {self.date}"


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="dish")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["name", "description", "price"], name="unique_dish"
            )
        ]


class Vote(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    vote_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["employee", "vote_date"], name="unique_employee_vote_per_day"
            )
        ]
