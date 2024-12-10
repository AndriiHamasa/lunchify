from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from vote_hub.models import Restaurant


RESTAURANT_URL = reverse("vote_hub:restaurant-list")


def sample_restaurant(**additional) -> Restaurant:
    defaults = {"name": "Restaurant Sample", "location": "Sample Location"}
    defaults.update(additional)
    return Restaurant.objects.create(**defaults)


def get_restaurant_detail(restaurant_id: int) -> str:
    return reverse("vote_hub:restaurant-detail", args=[restaurant_id])


class UnAuthenticatedRestaurantAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_restaurants(self):
        response = self.client.get(RESTAURANT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_detail(self):
        restaurant = sample_restaurant()

        response = self.client.get(get_restaurant_detail(restaurant.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRestaurantAPITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="test"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_restaurants(self):
        sample_restaurant()
        sample_restaurant(name="Restaurant 2", location="Location 2")

        response = self.client.get(RESTAURANT_URL)

        restaurants = Restaurant.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(restaurants))

    def test_restaurant_detail(self):
        restaurant = sample_restaurant()

        response = self.client.get(get_restaurant_detail(restaurant.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], restaurant.name)
        self.assertEqual(response.data["location"], restaurant.location)

    def test_create_update_delete_forbidden_restaurants(self):
        # create
        payload = {"name": "New Restaurant", "location": "New Location"}

        res_create = self.client.post(RESTAURANT_URL, payload)

        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)

        restaurant = sample_restaurant()

        # update
        url_update = get_restaurant_detail(restaurant.id)
        res_update = self.client.put(url_update, {"name": "Updated Restaurant"})
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)

        # delete
        url_delete = get_restaurant_detail(restaurant.id)
        res_delete = self.client.delete(url_delete)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)


class AdminRestaurantAPITests(TestCase):
    def setUp(self):
        self.payload = {"name": "New Restaurant", "location": "New Location"}
        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com", password="test"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_restaurant(self):
        res = self.client.post(RESTAURANT_URL, self.payload)
        restaurant = Restaurant.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.payload["name"], restaurant.name)
        self.assertEqual(self.payload["location"], restaurant.location)

    def test_update_restaurant(self):
        restaurant = sample_restaurant()
        self.payload["name"] = "Updated Restaurant"

        url = get_restaurant_detail(restaurant.id)

        res = self.client.put(url, self.payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_restaurant(self):
        restaurant = sample_restaurant()

        url = get_restaurant_detail(restaurant.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(restaurant, Restaurant.objects.all())
