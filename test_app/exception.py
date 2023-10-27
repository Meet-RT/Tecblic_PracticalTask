from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'User already exists.'
    default_code = 'UserAlreadyExists'


class UserNotExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'User Not Exists in System'
    default_code = 'UserNotExists'