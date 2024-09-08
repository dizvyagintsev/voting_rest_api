from .settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# vote weights decrease with each subsequent vote to same restaurant. last weight is for all subsequent votes
VOTE_WEIGHTS = (
    1.0,
    0.5,
    0.25,
)
# number of votes per user per day
DAILY_VOTE_LIMIT = 5
