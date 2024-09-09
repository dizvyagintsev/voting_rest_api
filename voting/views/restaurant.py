from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse404Serializer,
)
from rest_framework import generics, status
from rest_framework.pagination import CursorPagination

from voting.openapi_responses import BAD_REQUEST_RESPONSE_SCHEMA
from voting.repositories.restaurant import RestaurantRepository
from voting.serializers import RestaurantSerializer


class RestaurantPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
    ordering = "-created_at"


@extend_schema_view(
    get=extend_schema(
        tags=["restaurant"],
        summary="List all restaurants",
        responses={
            status.HTTP_200_OK: RestaurantSerializer(many=True),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                ErrorResponse404Serializer, description="Page not found."
            ),
        },
    ),
    post=extend_schema(
        tags=["restaurant"],
        summary="Create a new restaurant",
        responses={
            status.HTTP_201_CREATED: RestaurantSerializer,
            status.HTTP_400_BAD_REQUEST: BAD_REQUEST_RESPONSE_SCHEMA,
        },
    ),
)
class RestaurantListCreateView(generics.ListCreateAPIView):
    authentication_classes = []
    pagination_class = RestaurantPagination

    queryset = RestaurantRepository.all().order_by("created_at")
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save()


@extend_schema_view(
    get=extend_schema(
        tags=["restaurant"],
        summary="Retrieve a restaurant",
        responses={
            status.HTTP_200_OK: RestaurantSerializer,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
        },
    ),
    put=extend_schema(
        tags=["restaurant"],
        summary="Update a restaurant",
        responses={
            status.HTTP_200_OK: RestaurantSerializer,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
            status.HTTP_400_BAD_REQUEST: BAD_REQUEST_RESPONSE_SCHEMA,
        },
    ),
    delete=extend_schema(
        tags=["restaurant"],
        summary="Delete a restaurant",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
        },
    ),
    patch=extend_schema(
        tags=["restaurant"],
        summary="Partial update a restaurant",
        responses={
            status.HTTP_200_OK: RestaurantSerializer,
            status.HTTP_404_NOT_FOUND: ErrorResponse404Serializer,
            status.HTTP_400_BAD_REQUEST: BAD_REQUEST_RESPONSE_SCHEMA,
        },
    ),
)
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []

    queryset = RestaurantRepository.all()
    serializer_class = RestaurantSerializer
