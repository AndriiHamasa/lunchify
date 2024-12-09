from rest_framework import serializers
from datetime import date

from vote_hub.models import Restaurant, Menu, Vote, Dish


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "location")


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("name", "description", "price")


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, write_only=True)

    class Meta:
        model = Menu
        fields = ("id", "restaurant", "date", "dishes")

    def validate(self, attrs):
        restaurant = attrs.get("restaurant")

        if Menu.objects.filter(restaurant=restaurant, date=date.today()).exists():
            raise serializers.ValidationError(
                {
                    "detail": "A menu for this restaurant on this date already exists."}
            )

        return attrs

    def create(self, validated_data):
        dishes_data = validated_data.pop("dishes")
        menu = Menu.objects.create(**validated_data)

        for dish_data in dishes_data:
            Dish.objects.create(menu=menu, **dish_data)

        return menu


class ReadMenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(source="dish", many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ("id", "restaurant", "date", "dishes")


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("id", "employee", "menu", "vote_date")

    def validate(self, attrs):
        user = self.context['request'].user
        vote_date = date.today()

        if Vote.objects.filter(employee=user, vote_date=vote_date).exists():
            raise serializers.ValidationError("You have already voted today.")

        return attrs
