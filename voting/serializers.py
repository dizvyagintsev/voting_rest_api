import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ShortRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["restaurant", "created_at"]
        read_only_fields = ["created_at"]


class VotingListViewRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False, default=datetime.date.min)
    end_date = serializers.DateField(required=False, default=datetime.date.max)


class RestaurantVotingDetailSerializer(serializers.Serializer):
    restaurant = ShortRestaurantSerializer()
    distinct_user_count = serializers.IntegerField()
    weights_sum = serializers.FloatField()


class VotingSerializer(serializers.Serializer):
    date = serializers.DateField()
    restaurants = RestaurantVotingDetailSerializer(many=True)
    winner = ShortRestaurantSerializer()


# Overall response serializer that handles multiple voting entries
class VotingListViewResponseSerializer(serializers.Serializer):
    votings = VotingSerializer(many=True)


class RegisterUserRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "refresh", "access"]
        extra_kwargs = {
            "password": {"write_only": True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email"),
        )

        # Generate JWT token for the created user
        refresh = RefreshToken.for_user(user)

        return {
            "username": user.username,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
