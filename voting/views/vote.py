from typing import Any

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from lunch_voting.settings import DAILY_VOTE_LIMIT
from voting.models import Vote
from voting.repositories.vote import VoteRepository
from voting.serializers import VoteSerializer
from voting.services.vote import VoteService


@extend_schema(
    tags=["vote"],
    request=VoteSerializer,
    description="Vote for a restaurant.",
    responses={
        201: VoteSerializer,
        400: OpenApiResponse(
            description="Invalid input data or missing required fields."
        ),
        401: OpenApiResponse(description="Unauthorized."),
        403: OpenApiResponse(description="Forbidden: Daily vote limit reached."),
        404: OpenApiResponse(description="Not Found: Restaurant not found."),
    },
)
class VoteCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = request.user.id

        input_serializer = self.get_serializer(data=request.data)
        is_valid = input_serializer.is_valid(raise_exception=False)
        validated_data = input_serializer.validated_data

        if not is_valid:
            if (
                "restaurant" in request.data
                and "restaurant" not in input_serializer.validated_data
            ):
                return Response(
                    {"detail": "Restaurant not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "detail": "Invalid input data or missing required fields.",
                    "errors": input_serializer.errors,
                },
            )

        vote = VoteService(
            vote_repository=VoteRepository(),
            user_vote_limit=DAILY_VOTE_LIMIT,
        ).add_vote(
            user_id=user_id,
            restaurant_id=validated_data["restaurant"].id,
        )

        if not vote:
            return Response(
                {"detail": "Daily vote limit reached."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = VoteSerializer(vote)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
