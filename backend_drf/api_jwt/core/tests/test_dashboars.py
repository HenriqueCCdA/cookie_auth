import pytest
from dj_rest_auth.utils import jwt_encode
from django.shortcuts import resolve_url
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()
pytestmark = pytest.mark.django_db


def test_dashboard(client, user):

    url = resolve_url('get_user_info', user.uuid)

    access_token, _ = jwt_encode(user)

    client.cookies.load({'jwt-access-token': access_token})
    resp = client.get(url)
    body = resp.json()

    assert status.HTTP_200_OK == resp.status_code

    assert user.name == body['name']
    assert user.email == body['email']
    assert str(user.uuid) == body['uuid']
