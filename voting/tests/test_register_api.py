from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("testuser2")

    def test_register_user(self):
        """
        Ensure we can register a new user.
        """
        data = {"username": "testuser", "password": "testpassword"}
        url = reverse("register")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, "testuser")

    def test_register_user_same_username(self):
        """
        Ensure registering a user with invalid data fails.
        """
        data = {"username": "testuser2", "password": "testpassword"}
        url = reverse("register")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
