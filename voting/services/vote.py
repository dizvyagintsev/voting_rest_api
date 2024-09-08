import dataclasses
from collections import defaultdict
from typing import Iterator

from voting.models import Vote, Restaurant
from voting.repositories.restaurant import RestaurantRepository
from voting.repositories.vote import VoteRepository
from voting.serializers import VotingListViewResponseSerializer


@dataclasses.dataclass
class RestaurantVotingStats:
    distinct_user_count: int = 0
    weights_sum: float = 0.0


class VoteService:
    def __init__(
            self,
            vote_repository: VoteRepository,
            user_vote_limit: int,
    ):
        self.vote_repository = vote_repository
        self.user_vote_limit = user_vote_limit

    def add_vote(self, user_id: str, restaurant_id: int) -> Vote | None:
        """
        Add a vote to the restaurant. If the user has reached the limit of votes, it will return None.

        :param user_id: user id
        :param restaurant_id: restaurant id
        :return: Vote object if the vote was added, None otherwise
        """
        return self.vote_repository.add_vote(user_id, restaurant_id, self.user_vote_limit)
