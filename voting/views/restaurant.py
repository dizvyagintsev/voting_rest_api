from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from voting.repositories.restaurant import RestaurantRepository
from voting.serializers import RestaurantSerializer


@extend_schema(
    tags=["restaurant"],
    description="List and create restaurants",
    responses={
        201: RestaurantSerializer,
        400: OpenApiResponse(
            description="Invalid input data or missing required fields."
        ),
    },
)
class RestaurantListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

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
