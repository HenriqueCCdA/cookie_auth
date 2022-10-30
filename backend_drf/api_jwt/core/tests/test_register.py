import pytest
from django.shortcuts import resolve_url
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from api_jwt.core.tests.conftest import User, asserts_cookie_tokens

client = APIClient()
pytestmark = pytest.mark.django_db


@freeze_time('2022-01-01 00:00:00')
def test_register(client, user_data):

    user_data['confirmPassword'] = user_data['password']

    resp = client.post(resolve_url('register'), data=user_data)
    body = resp.json()

    assert status.HTTP_201_CREATED == resp.status_code

    user = User.objects.get(email=user_data['email'])

    assert OutstandingToken.objects.get(user=user)

    assert str(user.uuid) == body['uuid']
    assert user.name == body['name']
    assert user.email == body['email']

    asserts_cookie_tokens(resp)
