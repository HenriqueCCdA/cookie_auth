import pytest
from django.shortcuts import resolve_url
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from api_jwt.core.tests.conftest import asserts_cookie_tokens

client = APIClient()
pytestmark = pytest.mark.django_db


@freeze_time('2022-01-01 00:00:00')
def test_login(client, user, user_data):

    payload = {'email': user_data['email'], 'password': user_data['password']}

    resp = client.post(resolve_url('login'), data=payload)
    body = resp.json()

    assert status.HTTP_200_OK == resp.status_code

    assert OutstandingToken.objects.get(user=user)

    assert str(user.uuid) == body['uuid']

    asserts_cookie_tokens(resp)
