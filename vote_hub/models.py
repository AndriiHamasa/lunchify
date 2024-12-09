from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(null=False, blank=False)


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant")
    date = models.DateField(auto_now_add=True)
    items = models.ManyToManyField(Dish, related_name="menu", null=False)

    def __str__(self):
        return f"Menu for restaurant {self.restaurant.name} on {self.date}"


class Vote(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    vote_date = models.DateField(auto_now_add=True)
