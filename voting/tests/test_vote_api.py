from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from lunch_voting.test_settings import DAILY_VOTE_LIMIT
from voting.models import Restaurant, Vote


class VoteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.user).access_token}"
        )

        Restaurant.objects.create(name="Pizza Palace")

    def test_vote(self):
        response = self.client.post(reverse("vote-create"), {"restaurant": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.get().restaurant_id, 1)
        self.assertEqual(Vote.objects.get().user_id, self.user.id)

    def test_vote_nonexisting_restaurant(self):
        response = self.client.post(reverse("vote-create"), {"restaurant": 2})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Vote.objects.count(), 0)

    def test_exceed_vote_limit(self):
        for _ in range(DAILY_VOTE_LIMIT):
            response = self.client.post(reverse("vote-create"), {"restaurant": 1})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse("vote-create"), {"restaurant": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Vote.objects.count(), 5)
