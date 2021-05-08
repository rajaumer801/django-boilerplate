import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.conftest import api_client, authenticated_api_client  # noqa
from core.conftest import create_user  # noqa
from users.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserViewSet:
    endpoint = 'users'

    def test_list(self, authenticated_api_client):
        UserFactory.create_batch(3)
        endpoint = reverse(f'{self.endpoint}-list')
        response = authenticated_api_client.get(endpoint)

        assert response.status_code == 200
        assert len(response.json()) == 4

    def test_create(self, authenticated_api_client):
        user = UserFactory.build()
        expected_json = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'phone': user.phone,
        }
        endpoint = reverse(f'{self.endpoint}-list')
        response = authenticated_api_client.post(endpoint, data=expected_json,
                                                 format='json')
        data = response.json()
        del expected_json['password']
        del data['id']
        del data['photo']
        assert response.status_code == 201
        assert data == expected_json

    def test_retrieve(self, authenticated_api_client):
        user = UserFactory()
        expected_json = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'photo': None
        }
        endpoint = reverse(f'{self.endpoint}-detail',
                           kwargs={"pk": user.id})

        response = authenticated_api_client.get(endpoint)

        assert response.status_code == 405

    def test_update(self, authenticated_api_client):
        old_user = UserFactory()
        new_user = UserFactory.build()
        data = {
            'first_name': new_user.first_name,
            'last_name': new_user.last_name
        }

        endpoint = reverse(f'{self.endpoint}-detail',
                           kwargs={"pk": old_user.id})
        response = authenticated_api_client.put(endpoint, data=data,
                                                format="json")

        assert response.status_code == 200
        assert response.json()['first_name'] == new_user.first_name

    def test_delete(self, authenticated_api_client):
        user = UserFactory()
        endpoint = reverse(f'{self.endpoint}-detail',
                           kwargs={"pk": user.id})
        response = authenticated_api_client.delete(endpoint)

        assert response.status_code == 204
