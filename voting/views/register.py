from django.contrib.auth.models import User
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from voting.serializers import UserRegistrationSerializer


@extend_schema(
    tags=["register"],
    description="Register a new user",
    responses={
        201: UserRegistrationSerializer,
        400: OpenApiResponse(
            description="Invalid input data or missing required fields."
        ),
    },
)
class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
