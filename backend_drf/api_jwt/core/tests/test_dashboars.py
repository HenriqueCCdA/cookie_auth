import pytest
from dj_rest_auth.utils import jwt_encode
from django.shortcuts import resolve_url
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()
pytestmark = pytest.mark.django_db


def test_success(client, user):

    url = resolve_url('get_user_info', user.uuid)

    access_token, _ = jwt_encode(user)

    client.cookies.load({'jwt-access-token': access_token})
    resp = client.get(url)
    body = resp.json()

    assert status.HTTP_200_OK == resp.status_code

    assert user.name == body['name']
    assert user.email == body['email']
    assert str(user.uuid) == body['uuid']


def test_without_token(client, user):

    url = resolve_url('get_user_info', user.uuid)

    resp = client.get(url)
    body = resp.json()

    assert status.HTTP_401_UNAUTHORIZED == resp.status_code

    assert {'detail': 'Authentication credentials were not provided.'} == body


@freeze_time('2022-01-01 00:00:00', auto_tick_seconds=30)
def test_token_expired(client, user):

    url = resolve_url('get_user_info', user.uuid)

    access_token, _ = jwt_encode(user)

    client.cookies.load({'jwt-access-token': access_token})
    resp = client.get(url)
    body = resp.json()

    assert status.HTTP_401_UNAUTHORIZED == resp.status_code

    expected = {
        'code': 'token_not_valid',
        'detail': 'Given token not valid for any token type',
        'messages': [{'message': 'Token is invalid or expired', 'token_class': 'AccessToken', 'token_type': 'access'}],
    }

    assert expected == body
