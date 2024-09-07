import dataclasses
from collections import defaultdict

from django.db.models import QuerySet


@dataclasses.dataclass
class VoteStats:
    distinct_user_count: int = 0
    weights_sum: float = 0.0


def calculate_votings_stats(
        distinct_user_counts_per_restaurant: dict,
        user_votes_per_restaurant: QuerySet,
        weights: tuple[float, ...],
) -> dict[str, dict[int, VoteStats]]:
    votings_stats = defaultdict(lambda: defaultdict(VoteStats))

    for vote in user_votes_per_restaurant:
        vote_count = vote['vote_count']
        voting_date = vote['created_at__date']
        restaurant_id = vote['restaurant']

        weights_sum = calculate_weight(vote_count, weights)

        votings_stats[voting_date][restaurant_id].distinct_user_count = distinct_user_counts_per_restaurant.get(
            (voting_date, restaurant_id), 0
        )
        votings_stats[voting_date][restaurant_id].weights_sum += weights_sum

    return votings_stats


def calculate_weight(vote_count: int, weights: tuple[float, ...]) -> float:
    weights_sum = sum(weights[:vote_count]) + max(0, vote_count - len(weights)) * weights[-1]
    return weights_sum


def build_votings_list_response(restaurants, votings_stats):
    response = {"votings": []}
    for voting_date, restaurant_voting_stats in votings_stats.items():
        voting = {"date": voting_date}

        sorted_restaurants = sorted(
            restaurant_voting_stats.items(),
            key=lambda restaurant: (restaurant[1].weights_sum, restaurant[1].distinct_user_count),
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
    return response
