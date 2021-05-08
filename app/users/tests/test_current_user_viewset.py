import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.conftest import api_client, authenticated_api_client  # noqa
from core.conftest import create_user  # noqa
from users.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestCurrentUserViewSet:
    endpoint = 'me'

    def test_list(self, api_client):
        user = UserFactory()
        endpoint = reverse(f'{self.endpoint}-list')

        api_client.force_authenticate(user=user)
        response = api_client.get(endpoint)

        assert response.status_code == 200
        assert response.json()['username'] == user.username

    def test_update(self, api_client):
        user = UserFactory()
        data = {
            'first_name': "updated",
        }

        endpoint = reverse(f'{self.endpoint}-put')

        api_client.force_authenticate(user=user)
        response = api_client.put(endpoint, data=data,
                                  format="json")

        assert response.status_code == 200
        assert response.json()['first_name'] == data['first_name']
