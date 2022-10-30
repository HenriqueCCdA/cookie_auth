import pytest
from dj_rest_auth.utils import jwt_encode
from django.shortcuts import resolve_url
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

client = APIClient()
pytestmark = pytest.mark.django_db


def test_logout(client, user):

    access_token, refresh_token = jwt_encode(user)

    client.cookies.load({'jwt-access-token': access_token})
    client.cookies.load({'jwt-refresh-token': refresh_token})

    resp = client.post(resolve_url('logout'))
    body = resp.json()

    assert status.HTTP_200_OK == resp.status_code

    assert {'detail': 'Successfully logged out.'} == body

    assert OutstandingToken.objects.get(jti=refresh_token['jti'])
    assert BlacklistedToken.objects.get(token__jti=refresh_token['jti'])

    access_token = resp.cookies['jwt-access-token']
    refresh_token = resp.cookies['jwt-refresh-token']

    assert 'Thu, 01 Jan 1970 00:00:00 GMT' == access_token['expires']
    assert 'Thu, 01 Jan 1970 00:00:00 GMT' == refresh_token['expires']
