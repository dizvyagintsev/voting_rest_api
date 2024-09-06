import datetime

from rest_framework import serializers
from .models import Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ShortRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['restaurant', 'created_at']
        read_only_fields = ['created_at']


class VotingListViewRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False, default=datetime.date.min)
    end_date = serializers.DateField(required=False, default=datetime.date.max)


class RestaurantVotingDetailSerializer(serializers.Serializer):
    restaurant = ShortRestaurantSerializer()  # Use the nested restaurant serializer
    distinct_user_count = serializers.IntegerField()
    weights_sum = serializers.FloatField()


class VotingSerializer(serializers.Serializer):
    date = serializers.DateField()  # Assuming you're dealing with date strings in "YYYY-MM-DD" format
    restaurants = RestaurantVotingDetailSerializer(many=True)  # List of restaurant details for that day
    winner = ShortRestaurantSerializer()  # The winning restaurant


# Overall response serializer that handles multiple voting entries
class VotingListViewResponseSerializer(serializers.Serializer):
    votings = VotingSerializer(many=True)

