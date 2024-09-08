from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from lunch_voting.settings import VOTE_WEIGHTS
from voting.repositories.restaurant import RestaurantRepository
from voting.repositories.vote import VoteRepository
from voting.serializers import (
    VotingListViewRequestSerializer,
    VotingListViewResponseSerializer,
)
from voting.services.voting_stats import VotingStatsService


@extend_schema(
    tags=["vote"],
    parameters=[
        OpenApiParameter(
            name="start_date",
            description="Start date for filtering",
            required=False,
            type=OpenApiTypes.DATE,
        ),
        OpenApiParameter(
            name="end_date",
            description="End date for filtering",
            required=False,
            type=OpenApiTypes.DATE,
        ),
    ],
    description="Get voting list for the given date range.",
    responses={
        200: VotingListViewResponseSerializer,
        400: "Invalid input data or missing required fields.",
    },
)
class VotingListView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = VotingListViewRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        votings = VotingStatsService(
            vote_repository=VoteRepository(),
            restaurant_repository=RestaurantRepository(),
            weights=VOTE_WEIGHTS,
        ).get_voting_list_by_date(
            start_date=serializer.validated_data["start_date"],
            end_date=serializer.validated_data["end_date"],
        )

        return Response(votings.data)
