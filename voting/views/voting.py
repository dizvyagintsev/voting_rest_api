import dataclasses
from collections import defaultdict

from django.db import models
from drf_spectacular.utils import extend_schema
from rest_framework import views
from rest_framework.response import Response

from voting.models import Vote, Restaurant
from voting.serializers import VotingListViewRequestSerializer, VotingListViewResponseSerializer


@dataclasses.dataclass
class VoteStats:
    distinct_user_count: int = 0
    weights_sum: float = 0.0


WEIGHTS = [1.0, 0.5, 0.25]


@extend_schema(
    request=VotingListViewRequestSerializer,
    responses=VotingListViewResponseSerializer,
)
class VotingListView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = VotingListViewRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        date_filtered_votes = Vote.objects.filter(
            created_at__date__range=(serializer.validated_data['start_date'], serializer.validated_data['end_date'])
        )
        restaurant_ids = date_filtered_votes.distinct('restaurant').values_list('restaurant', flat=True)
        restaurant_details = {
            restaurant.id: restaurant for restaurant in Restaurant.objects.filter(id__in=restaurant_ids)
        }

        grouped_votes = date_filtered_votes.values('created_at__date', 'user_id', 'restaurant').annotate(
            vote_count=models.Count('user_id'),
        ).order_by('-created_at__date')

        distinct_users = grouped_votes.values('created_at__date', 'restaurant').annotate(
            distinct_user_count=models.Count('user_id', distinct=True),
        )

        distinct_users_count = {
            (distinct_user['created_at__date'], distinct_user['restaurant']): distinct_user['distinct_user_count']
            for distinct_user in distinct_users
        }

        votings = defaultdict(lambda: defaultdict(VoteStats))

        for grouped_vote in grouped_votes:
            voting_date, user_id, restaurant_id, vote_count = (
                grouped_vote['created_at__date'],
                grouped_vote['user_id'],
                grouped_vote['restaurant'],
                grouped_vote['vote_count'],
            )

            weights_sum = sum(WEIGHTS[:vote_count]) + max(0, vote_count - len(WEIGHTS)) * WEIGHTS[-1]

            votings[voting_date][restaurant_id].distinct_user_count = distinct_users_count.get(
                (voting_date, restaurant_id), 0
            )
            votings[voting_date][restaurant_id].weights_sum += weights_sum

        response = {"votings": []}

        for voting_date, restaurants in votings.items():
            voting = {"date": voting_date}

            sorted_restaurants = sorted(
                restaurants.items(),
                key=lambda restaurant: (restaurant[1].weights_sum, restaurant[1].distinct_user_count),
                reverse=True,
            )

            voting["restaurants"] = [
                {
                    "restaurant": restaurant_details[restaurant_id],
                    **dataclasses.asdict(stats),
                }
                for restaurant_id, stats in sorted_restaurants
            ]

            voting["winner"] = voting["restaurants"][0]["restaurant"]

            response["votings"].append(voting)

        serializer = VotingListViewResponseSerializer(response)

        return Response(serializer.data)
