import datetime
from typing import Iterator

from django.db import models, transaction
from django.db.models import QuerySet
from django.utils import timezone

from voting.models import Vote


class VoteRepository:
    @transaction.atomic
    def add_vote(
        self, user_id: int, restaurant_id: int, user_vote_limit: int
    ) -> Vote | None:
        """
        Add record to the vote table and return the vote object if the user has not reached the limit of votes.

        :param user_id: user id
        :param restaurant_id: restaurant id
        :param user_vote_limit: user vote limit
        :return: Vote object if the vote was added, None otherwise
        """
        today = timezone.now().date()

        votes_count = (
            Vote.objects.select_for_update()
            .filter(
                user_id=user_id, restaurant_id=restaurant_id, created_at__date=today
            )
            .count()
        )

        if votes_count >= user_vote_limit:
            return None

        return Vote.objects.create(user_id=user_id, restaurant_id=restaurant_id)

    @staticmethod
    def query_votes_by_date(
        start_date: datetime.date, end_date: datetime.date
    ) -> QuerySet[Vote]:
        """
        Query votes by date.

        :param start_date: start date
        :param end_date: end date
        :return: votes by date
        """
        return Vote.objects.filter(created_at__date__range=(start_date, end_date))

    @staticmethod
    def get_user_votes_count_per_restaurant(votes: QuerySet[Vote]) -> Iterator[dict]:
        """
        Get count of specific user votes per restaurant.

        :param votes: votes
        :return: count of user votes per restaurant
        """
        return (
            votes.values("created_at__date", "restaurant", "user_id")
            .annotate(
                vote_count=models.Count("user_id"),
            )
            .order_by("-created_at__date")
            .iterator()
        )

    @staticmethod
    def get_distinct_users_votes_count_per_restaurant(
        votes: QuerySet[Vote],
    ) -> Iterator[dict]:
        """
        Get count of distinct users votes per restaurant.

        :param votes: votes
        :return: count of distinct users votes per restaurant
        """
        return (
            votes.values("created_at__date", "restaurant")
            .annotate(distinct_user_count=models.Count("user_id", distinct=True))
            .iterator()
        )
