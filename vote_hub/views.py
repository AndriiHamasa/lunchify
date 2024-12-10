from datetime import date

from rest_framework import viewsets
from django.db.models import Count

from vote_hub.models import Restaurant, Menu, Vote, Dish
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from vote_hub.permissions import IsAdminOrAuthenticatedForReading
from vote_hub.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializer,
    ReadMenuSerializer,
    DishSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrAuthenticatedForReading,)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrAuthenticatedForReading,)

    def get_serializer_class(self):
        if self.action == "current":
            return ReadMenuSerializer
        else:
            return MenuSerializer

    def get_queryset(self):
        if self.action == "current":
            return Menu.objects.filter(date=date.today()).prefetch_related("dish")
        return super().get_queryset()

    @action(
        methods=["GET"],
        detail=False,
        url_path="current",
        permission_classes=(IsAuthenticated,),
    )
    def current(self, request, *args, **kwargs):
        """Endpoint for getting menu of current day"""

        menu_list = self.get_queryset()

        serializer = self.get_serializer(menu_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="winner",
        permission_classes=(IsAuthenticated,),
    )
    def winner(self, request, *args, **kwargs):
        """Endpoint for getting menu, that has the biggest amount of votes"""
        menu_votes = (
            Vote.objects.values("menu__id", "menu__restaurant__name")
            .annotate(vote_count=Count("id"))
            .order_by("-vote_count")
        )

        if not menu_votes:
            return Response(
                {"detail": "No votes have been cast yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        top_menu = menu_votes[0]
        top_menu_id = top_menu["menu__id"]

        dishes = Dish.objects.filter(menu=top_menu_id)
        dish_serializer = DishSerializer(dishes, many=True)
        return Response(
            {
                "menu_id": top_menu_id,
                "votes": top_menu["vote_count"],
                "dishes": dish_serializer.data,
                "restaurant_name": top_menu["menu__restaurant__name"],
            },
            status=status.HTTP_200_OK,
        )


class VoteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)
