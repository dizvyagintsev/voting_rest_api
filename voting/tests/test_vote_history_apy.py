from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from voting.models import Restaurant, Vote


class VoteHistoryTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="test1", password="test")
        user2 = User.objects.create_user(username="test2", password="test")
        user3 = User.objects.create_user(username="test3", password="test")

        restaurant1 = Restaurant.objects.create(name="Pizza Palace")
        restaurant2 = Restaurant.objects.create(name="Burger Bar")

        votes = [
            Vote.objects.create(user_id=user1.id, restaurant_id=restaurant1.id)
            for _ in range(4)
        ] + [
            Vote.objects.create(user_id=user2.id, restaurant_id=restaurant2.id),
            Vote.objects.create(user_id=user3.id, restaurant_id=restaurant2.id),
        ]

        dates = {vote.created_at.date() for vote in votes}
        self.assertEqual(len(dates), 1)
        self.date = dates.pop()

    def test_get_vote_history(self):
        response = self.client.get(reverse("voting-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "votings": [
                    {
                        "date": str(self.date),
                        "restaurants": [
                            {
                                "restaurant": {"id": 2, "name": "Burger Bar"},
                                "distinct_user_count": 2,
                                "weights_sum": 2.0,
                            },
                            {
                                "restaurant": {"id": 1, "name": "Pizza Palace"},
                                "distinct_user_count": 1,
                                "weights_sum": 2.0,
                            },
                        ],
                        "winner": {"id": 2, "name": "Burger Bar"},
                    },
                ]
            },
        )
