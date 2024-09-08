from drf_spectacular.utils import extend_schema
from rest_framework import views
from rest_framework.response import Response

from voting.repositories.restaurant import RestaurantRepository
from voting.repositories.vote import VoteRepository
from voting.serializers import VotingListViewRequestSerializer, VotingListViewResponseSerializer
from voting.services.voting_stats import VotingStatsService

WEIGHTS = (1.0, 0.5, 0.25,)


@extend_schema(
    request=VotingListViewRequestSerializer,
    responses=VotingListViewResponseSerializer,
)
class VotingListView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = VotingListViewRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        votings = VotingStatsService(
            vote_repository=VoteRepository(),
            restaurant_repository=RestaurantRepository(),
            weights=WEIGHTS,
        ).get_voting_list_by_date(
            start_date=serializer.validated_data['start_date'],
            end_date=serializer.validated_data['end_date'],
        )

        return Response(votings.data)
