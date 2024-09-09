from typing import Any

from drf_spectacular.utils import OpenApiResponse, extend_schema
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse401Serializer,
    ErrorResponse403Serializer,
)
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from lunch_voting.settings import DAILY_VOTE_LIMIT
from voting.models import Vote
from voting.openapi_responses import BAD_REQUEST_RESPONSE_SCHEMA
from voting.repositories.vote import VoteRepository
from voting.serializers import VoteSerializer
from voting.services.vote import VoteService


@extend_schema(
    tags=["vote"],
    summary="Vote for a restaurant",
    responses={
        status.HTTP_201_CREATED: VoteSerializer,
        status.HTTP_400_BAD_REQUEST: BAD_REQUEST_RESPONSE_SCHEMA,
        status.HTTP_401_UNAUTHORIZED: ErrorResponse401Serializer,
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            ErrorResponse403Serializer, description="Daily vote limit reached."
        ),
    },
)
class VoteCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = request.user.id

        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        vote = VoteService(
            vote_repository=VoteRepository(),
            user_vote_limit=DAILY_VOTE_LIMIT,
        ).add_vote(
            user_id=user_id,
            restaurant_id=validated_data["restaurant"].id,
        )

        if not vote:
            serializer = ErrorResponse403Serializer(
                {
                    "type": "client_error",
                    "errors": [
                        {
                            "code": "permission_denied",
                            "detail": "Daily vote limit reached.",
                            "attr": None,
                        }
                    ],
                }
            )

            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

        serializer = VoteSerializer(vote)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
