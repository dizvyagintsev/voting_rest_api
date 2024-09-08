import dataclasses
import datetime
from collections import defaultdict
from typing import Iterator, Any

from voting.models import Restaurant
from voting.repositories.restaurant import RestaurantRepository
from voting.repositories.vote import VoteRepository
from voting.serializers import VotingListViewResponseSerializer
from voting.services.vote import RestaurantVotingStats


class VotingStatsService:
    def __init__(
        self,
        vote_repository: VoteRepository,
        restaurant_repository: RestaurantRepository,
        weights: tuple[float, ...],
    ):
        self.vote_repository = vote_repository
        self.restaurant_repository = restaurant_repository
        self.weights = weights

    def get_voting_list_by_date(
        self, start_date, end_date
    ) -> VotingListViewResponseSerializer:
        """
        Get votings list for the given date range. Calculate voting statistics for each restaurant for each voting date.

        :param start_date: start date
        :param end_date: end date
        :return: votings list response
        """
        votes_query = self.vote_repository.query_votes_by_date(start_date, end_date)

        user_votes_count_per_restaurant = (
            self.vote_repository.get_user_votes_count_per_restaurant(votes_query)
        )
        distinct_users_votes_count_per_restaurant = (
            self.vote_repository.get_distinct_users_votes_count_per_restaurant(
                votes_query
            )
        )

        votings_stats, restaurant_ids = self._calculate_voting_stats(
            distinct_users_votes_count_per_restaurant,
            user_votes_count_per_restaurant,
        )

        restaurants = {
            restaurant.id: restaurant
            for restaurant in self.restaurant_repository.get_by_ids(restaurant_ids)
        }

        return self._build_voting_list_response(restaurants, votings_stats)

    def _calculate_voting_stats(
        self,
        distinct_user_counts_per_restaurant: Iterator[dict],
        user_votes_per_restaurant: Iterator[dict],
    ) -> tuple[dict[str, dict[int, RestaurantVotingStats]], set[int]]:
        """
        Calculate voting statistics for each restaurant for each voting date.

        :param distinct_user_counts_per_restaurant: iterator of user votes count per restaurant
        :param user_votes_per_restaurant: iterator of distinct users voted count per restaurant
        :return: Voting statistics (distinct user count, weights sum) for each restaurant for each voting date and
                    set of voted restaurant ids
        """
        votings_stats: dict[str, dict[int, RestaurantVotingStats]] = defaultdict(
            lambda: defaultdict(RestaurantVotingStats)
        )

        distinct_users_count_lookup = {
            (
                distinct_user["created_at__date"],
                distinct_user["restaurant"],
            ): distinct_user["distinct_user_count"]
            for distinct_user in distinct_user_counts_per_restaurant
        }

        voted_restaurant_ids = set()

        for vote in user_votes_per_restaurant:
            vote_count = vote["vote_count"]
            voting_date = vote["created_at__date"]
            restaurant_id = vote["restaurant"]

            weights_sum = self._calculate_weight(vote_count)

            votings_stats[voting_date][
                restaurant_id
            ].distinct_user_count = distinct_users_count_lookup.get(
                (voting_date, restaurant_id), 0
            )
            votings_stats[voting_date][restaurant_id].weights_sum += weights_sum

            voted_restaurant_ids.add(restaurant_id)

        return votings_stats, voted_restaurant_ids

    def _calculate_weight(self, vote_count: int) -> float:
        weights_sum = (
            sum(self.weights[:vote_count])
            + max(0, vote_count - len(self.weights)) * self.weights[-1]
        )
        return weights_sum

    @staticmethod
    def _build_voting_list_response(
        restaurants: dict[int, Restaurant],
        votings_stats: dict[str, dict[int, RestaurantVotingStats]],
    ) -> VotingListViewResponseSerializer:
        response: dict[str, list[dict]] = {"votings": []}
        for voting_date, restaurant_voting_stats in votings_stats.items():
            voting: dict = {"date": voting_date}

            sorted_restaurants = sorted(
                restaurant_voting_stats.items(),
                key=lambda restaurant: (
                    restaurant[1].weights_sum,
                    restaurant[1].distinct_user_count,
                ),
                reverse=True,
            )

            voting["restaurants"] = [
                {
                    "restaurant": restaurants[restaurant_id],
                    **dataclasses.asdict(stats),
                }
                for restaurant_id, stats in sorted_restaurants
            ]

            voting["winner"] = voting["restaurants"][0]["restaurant"]

            response["votings"].append(voting)

        return VotingListViewResponseSerializer(response)
