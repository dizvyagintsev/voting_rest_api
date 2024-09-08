from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from voting.repositories.restaurant import RestaurantRepository
from voting.serializers import RestaurantSerializer


class RestaurantPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


@extend_schema(
    tags=["restaurant"],
    description="List and create restaurants",
    responses={
        201: RestaurantSerializer,
        400: OpenApiResponse(
            description="Invalid input data or missing required fields."
        ),
    },
    parameters=[
        OpenApiParameter(name='page', description='Page number for pagination', required=False, type=int),
        OpenApiParameter(name='page_size', description='Number of items per page', required=False, type=int),
    ],
)
class RestaurantListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class = RestaurantPagination

    queryset = RestaurantRepository.all()
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save()


@extend_schema(
    tags=["restaurant"],
    description="Retrieve, update and delete a restaurant",
    responses={
        200: RestaurantSerializer,
        400: OpenApiResponse(
            description="Invalid input data or missing required fields."
        ),
        404: OpenApiResponse(description="Not Found: Restaurant not found."),
    },
)
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    queryset = RestaurantRepository.all()
    serializer_class = RestaurantSerializer
