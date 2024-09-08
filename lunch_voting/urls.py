"""
URL configuration for lunch_voting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from voting.views.restaurant import RestaurantListCreateView, RestaurantDetailView
from voting.views.vote import VoteCreateView
from voting.views.voting import VotingListView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/v1/restaurants/', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('api/v1/restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),

    path('api/v1/vote/', VoteCreateView.as_view(), name='vote-create'),

    path('api/v1/votings/', VotingListView.as_view(), name='voting-list'),
]
