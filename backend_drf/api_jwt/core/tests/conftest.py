import pytest
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.fixture
def user_data():
    return dict(
        name=fake.name(),
        password=fake.password(),
        email=fake.email(),
    )


@pytest.fixture
def user(user_data):
    return User.objects.create_user(**user_data)


def asserts_cookie_tokens(resp):
    access_token = resp.cookies['jwt-access-token']
    refresh_token = resp.cookies['jwt-refresh-token']

    assert '/' == access_token['path']
    assert access_token['httponly']
    assert 'Lax' == access_token['samesite']
    assert 'Sat, 01 Jan 2022 00:00:31 GMT' == access_token['expires']

    assert '/token' == refresh_token['path']
    assert refresh_token['httponly']
    assert 'Lax' == refresh_token['samesite']
    assert 'Sat, 01 Jan 2022 00:01:01 GMT' == refresh_token['expires']
