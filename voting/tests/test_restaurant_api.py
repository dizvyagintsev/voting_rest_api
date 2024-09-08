from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from voting.models import Restaurant


class RestaurantTests(APITestCase):
    def setUp(self):
        # Set up initial data, e.g., creating a few restaurant objects for testing
        self.restaurant1 = Restaurant.objects.create(name="Pizza Palace")
        self.restaurant2 = Restaurant.objects.create(name="Burger Shack")

    def test_list_restaurants(self):
        """
        Ensure we can retrieve a list of restaurants.
        """
        url = reverse("restaurant-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], self.restaurant1.name)
        self.assertEqual(response.data[1]["name"], self.restaurant2.name)

    def test_retrieve_restaurant(self):
        """
        Ensure we can retrieve a single restaurant.
        """
        url = reverse("restaurant-detail", kwargs={"pk": self.restaurant1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.restaurant1.name)

    def test_create_restaurant(self):
        """
        Ensure we can create a new restaurant.
        """
        data = {"name": "Sushi Spot"}
        url = reverse("restaurant-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 3)
        self.assertEqual(
            Restaurant.objects.get(id=response.data["id"]).name, "Sushi Spot"
        )

    def test_create_restaurant_invalid(self):
        """
        Ensure creating a restaurant with invalid data fails.
        """
        data = {"name": ""}
        url = reverse("restaurant-list-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_restaurant(self):
        """
        Ensure we can update a restaurant's details.
        """
        url = reverse("restaurant-detail", kwargs={"pk": self.restaurant1.pk})
        data = {"name": "Pizza Castle"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant1.refresh_from_db()
        self.assertEqual(self.restaurant1.name, "Pizza Castle")

    def test_update_restaurant_invalid(self):
        """
        Ensure updating a restaurant with invalid data fails.
        """
        url = reverse("restaurant-detail", kwargs={"pk": self.restaurant1.pk})
        data = {"name": ""}  # Invalid update
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_restaurant(self):
        """
        Ensure updating a non-existent restaurant returns a 404.
        """
        url = reverse("restaurant-detail", kwargs={"pk": 999})
        data = {"name": "Pizza Castle"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_restaurant(self):
        """
        Ensure we can delete a restaurant.
        """
        url = reverse("restaurant-detail", kwargs={"pk": self.restaurant1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Restaurant.objects.count(), 1
        )  # Only 1 restaurant should remain

    def test_delete_nonexistent_restaurant(self):
        """
        Ensure deleting a non-existent restaurant returns a 404.
        """
        url = reverse("restaurant-detail", kwargs={"pk": 999})  # Non-existent ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
