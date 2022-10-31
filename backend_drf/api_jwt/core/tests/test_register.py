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
def test_success(client, user_data):

    user_data['password2'] = user_data['password']

    resp = client.post(resolve_url('register'), data=user_data)
    body = resp.json()

    assert status.HTTP_201_CREATED == resp.status_code

    user = User.objects.get(email=user_data['email'])

    assert OutstandingToken.objects.get(user=user)

    assert str(user.uuid) == body['uuid']
    assert user.name == body['name']
    assert user.email == body['email']

    assert 'password' not in body

    asserts_cookie_tokens(resp)


@pytest.mark.parametrize(
    'field, error',
    [
        ('email', {'email': ['This field is required.']}),
        ('name', {'name': ['This field is required.']}),
        ('password', {'password': ['This field is required.']}),
        ('password2', {'password2': ['This field is required.']}),
    ],
)
def test_fail_missing_fieldsl(field, error, client, user_data):

    user_data['password2'] = user_data['password']

    user_data.pop(field)

    resp = client.post(resolve_url('register'), data=user_data)
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert error == body


def test_fail_email_already_exists(client, user, user_data):

    user_data['password2'] = user_data['password']

    resp = client.post(resolve_url('register'), data=user_data)
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert {'email': ['user with this email address already exists.']} == body


@pytest.mark.parametrize(
    'password, error',
    [
        ('15684568', {'non_field_errors': ['This password is entirely numeric.']}),
        ('ads2', {'non_field_errors': ['This password is too short. It must contain at least 8 characters.']}),
    ],
)
def test_fail_password(password, error, client, user_data):

    user_data['password'] = password
    user_data['password2'] = user_data['password']

    resp = client.post(resolve_url('register'), data=user_data)
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert error == body


def test_invalid_email(client, user_data):

    user_data['email'] = 'useremail.com'
    user_data['password2'] = user_data['password']

    resp = client.post(resolve_url('register'), data=user_data)
    body = resp.json()

    assert status.HTTP_400_BAD_REQUEST == resp.status_code

    assert {'email': ['Enter a valid email address.']} == body
