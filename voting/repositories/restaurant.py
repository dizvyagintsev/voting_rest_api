from typing import Iterator, Iterable

from django.db.models import QuerySet

from voting.models import Restaurant


class RestaurantRepository:
    @staticmethod
    def all() -> QuerySet[Restaurant]:
        """
        query all restaurants.

        :return: queryset of all restaurants
        """
        return Restaurant.objects.all()

    @staticmethod
    def get_by_ids(restaurant_ids: Iterable[int]) -> Iterator[Restaurant]:
        """
        Get restaurants by ids.

        :param restaurant_ids: restaurant ids
        :return: restaurants
        """
        return Restaurant.objects.filter(id__in=restaurant_ids).iterator()