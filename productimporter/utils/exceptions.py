from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    """Custom exception class to return API3 conformant errors"""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ""
    errors = None

    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        code="BAD REQUEST",
        message=None,
        errors=None,
    ):
        self.status_code = status_code
        self.default_code = code
        self.detail = self.default_detail
        if message:
            self.detail = message
        self.errors = errors