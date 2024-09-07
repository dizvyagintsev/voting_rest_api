from django.db import models
from drf_spectacular.utils import extend_schema
from rest_framework import views
from rest_framework.response import Response

from voting.models import Vote, Restaurant
from voting.serializers import VotingListViewRequestSerializer, VotingListViewResponseSerializer
from voting.utils import calculate_votings_stats, build_votings_list_response

WEIGHTS = (1.0, 0.5, 0.25,)


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
        ).values('restaurant_id', 'created_at__date', 'user_id')

        restaurant_ids = date_filtered_votes.distinct('restaurant').values_list('restaurant', flat=True)
        restaurants = {
            restaurant.id: restaurant for restaurant in Restaurant.objects.filter(id__in=restaurant_ids)
        }

        user_votes_per_restaurant = date_filtered_votes.values('created_at__date', 'user_id', 'restaurant').annotate(
            vote_count=models.Count('user_id'),
        ).order_by('-created_at__date')

        distinct_user_counts_per_restaurant = {
            (distinct_user['created_at__date'], distinct_user['restaurant']): distinct_user['distinct_user_count']
            for distinct_user in user_votes_per_restaurant.values('created_at__date', 'restaurant').annotate(
                distinct_user_count=models.Count('user_id', distinct=True)
            )
        }

        votings_stats = calculate_votings_stats(distinct_user_counts_per_restaurant, user_votes_per_restaurant, WEIGHTS)

        response = build_votings_list_response(restaurants, votings_stats)

        serializer = VotingListViewResponseSerializer(response)

        return Response(serializer.data)
