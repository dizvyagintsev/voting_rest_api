from typing import Any

from django.db import transaction
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from voting.models import Vote
from voting.serializers import VoteSerializer

DAILY_VOTE_LIMIT = 5
WEIGHTS = [1.0, 0.5, 0.25]


@extend_schema(
    request=VoteSerializer,
    responses={201: VoteSerializer},
    parameters=[
        OpenApiParameter(
            name='X-User-Id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.HEADER,
            required=True,
            description='User ID passed in the header',
            default=1,
        ),
    ]
)
class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = request.headers.get('X-User-Id')
        if not user_id:
            raise AuthenticationFailed("Unauthenticated: X-User-Id header is required.")

        input_serializer = self.get_serializer(data=request.data)
        is_valid = input_serializer.is_valid(raise_exception=False)
        validated_data = input_serializer.validated_data

        if not is_valid:
            if "restaurant" in request.data and "restaurant" not in input_serializer.validated_data:
                return Response(
                    {"detail": "Restaurant not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        today = timezone.now().date()

        with transaction.atomic():
            votes = Vote.objects.select_for_update().filter(
                user_id=user_id,
                created_at__date=today
            )

            daily_vote_count = votes.count()

            if daily_vote_count >= DAILY_VOTE_LIMIT:
                message = f"Vote limit reached for today. You can only vote {DAILY_VOTE_LIMIT} times per day."
                return Response(
                    {"detail": message},
                    status=status.HTTP_403_FORBIDDEN
                )

            vote = Vote(
                user_id=user_id,
                restaurant=validated_data["restaurant"],
            )

            vote.save()

        serializer = VoteSerializer(vote)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
