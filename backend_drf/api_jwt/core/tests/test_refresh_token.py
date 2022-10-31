import pytest
from dj_rest_auth.utils import jwt_encode
from django.shortcuts import resolve_url
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from api_jwt.core.tests.conftest import asserts_cookie_tokens

client = APIClient()
pytestmark = pytest.mark.django_db


@freeze_time('2022-01-01 00:00:00')
def test_refresh_token(client, user):

    url = resolve_url('token_refresh')

    _, refresh_token = jwt_encode(user)

    client.cookies.load({'jwt-refresh-token': refresh_token})
    resp = client.post(url)

    assert status.HTTP_200_OK == resp.status_code

    asserts_cookie_tokens(resp)


def test_missing_token(client):

    url = resolve_url('token_refresh')

    resp = client.post(url)
    body = resp.json()

    assert status.HTTP_401_UNAUTHORIZED == resp.status_code

    assert {'code': 'token_not_valid', 'detail': 'No valid refresh token found.'} == body


@freeze_time('2022-01-01 00:00:00', auto_tick_seconds=5 * 60)
def test_token_expired(client, user):

    url = resolve_url('token_refresh')

    _, refresh_token = jwt_encode(user)

    client.cookies.load({'jwt-refresh-token': refresh_token})
    resp = client.post(url)

    assert status.HTTP_401_UNAUTHORIZED == resp.status_code
    body = resp.json()

    assert {'code': 'token_not_valid', 'detail': 'Token is invalid or expired'} == body
