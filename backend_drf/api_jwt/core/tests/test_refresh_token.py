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
