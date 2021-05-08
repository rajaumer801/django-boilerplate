import pytest
from django.urls import reverse

from core.conftest import api_client  # noqa
from users.factories import UserFactory


@pytest.mark.django_db
def test_change_password(api_client):
    user = UserFactory(password="my-pass")
    data = {
        'old_password': "my-pass",
        'new_password': "my-new-pass"
    }
    endpoint = reverse('change-password')
    api_client.force_authenticate(user=user)
    response = api_client.put(endpoint, data=data, format="json")
    assert response.status_code == 200
