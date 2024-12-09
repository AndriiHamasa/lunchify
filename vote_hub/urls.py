from rest_framework import routers
from django.urls import path, include

from vote_hub.views import RestaurantViewSet, MenuViewSet, VoteViewSet

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menu", MenuViewSet)
router.register("vote", VoteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "vote_hub"
