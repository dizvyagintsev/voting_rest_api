from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.generics import CreateAPIView

from voting.openapi_responses import BAD_REQUEST_RESPONSE_SCHEMA
from voting.serializers import UserRegistrationSerializer


@extend_schema(
    tags=["register"],
    summary="Register a new user",
    responses={
        status.HTTP_201_CREATED: UserRegistrationSerializer,
        status.HTTP_400_BAD_REQUEST: BAD_REQUEST_RESPONSE_SCHEMA,
    },
)
class RegisterUserView(CreateAPIView):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
