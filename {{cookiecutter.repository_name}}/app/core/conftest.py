import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from users.factories import UserFactory


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return UserFactory(is_staff=True)
    return make_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


register(UserFactory)
