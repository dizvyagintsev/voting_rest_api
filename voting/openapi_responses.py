from drf_spectacular.utils import OpenApiResponse, PolymorphicProxySerializer
from drf_standardized_errors.openapi_serializers import (
    ParseErrorResponseSerializer,
    ValidationErrorResponseSerializer,
)

BAD_REQUEST_RESPONSE_SCHEMA = OpenApiResponse(
    PolymorphicProxySerializer(
        serializers=[
            ValidationErrorResponseSerializer,
            ParseErrorResponseSerializer,
        ],
        resource_type_field_name="type",
        component_name="ErrorResponse400",
    ),
    description="Input data can't be processed.",
)
