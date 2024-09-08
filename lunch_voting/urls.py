from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from voting.views.register import RegisterUserView
from voting.views.restaurant import RestaurantDetailView, RestaurantListCreateView
from voting.views.vote import VoteCreateView
from voting.views.voting import VotingListView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/register/", RegisterUserView.as_view(), name="register"),
    path(
        "api/v1/restaurants/",
        RestaurantListCreateView.as_view(),
        name="restaurant-list-create",
    ),
    path(
        "api/v1/restaurants/<int:pk>/",
        RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
    path("api/v1/votes/", VoteCreateView.as_view(), name="vote-create"),
    path("api/v1/votes-history/", VotingListView.as_view(), name="voting-list"),
]
