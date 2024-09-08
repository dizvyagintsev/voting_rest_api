from rest_framework import generics

from voting.models import Restaurant
from voting.repositories.restaurant import RestaurantRepository
from voting.serializers import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = RestaurantRepository.all()
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save()


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantRepository.all()
    serializer_class = RestaurantSerializer

