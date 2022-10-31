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


def test_fail_login_without_username_or_password(client, user):

    resp = client.post(resolve_url('login'), data={})
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert not OutstandingToken.objects.exists()

    assert {'password': ['This field is required.']} == body


def test_fail_login_without_username(client, user_data, user):

    resp = client.post(resolve_url('login'), data={'password': user_data['password']})
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert not OutstandingToken.objects.exists()

    assert {'non_field_errors': ['Unable to log in with provided credentials.']} == body


def test_fail_login_without_register_user(client, user_data):

    payload = {'email': user_data['email'], 'password': user_data['password']}

    resp = client.post(resolve_url('login'), data=payload)
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert not OutstandingToken.objects.exists()

    assert {'non_field_errors': ['Unable to log in with provided credentials.']} == body
