import pytest
from django.urls import reverse

from core.conftest import api_client  # noqa
from users.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email, password, status_code', [
        ('user@example.com', 'invalid_pass', 400),
        pytest.param(
            None, None, 400,
            marks=pytest.mark.bad_request
        ),
        pytest.param(
            None, 'strong_pass', 400,
            marks=pytest.mark.bad_request,
            id='bad_request_with_pass'
        ),
        pytest.param(
            'some@magic.email', None, 400,
            marks=[
                pytest.mark.bad_request,
                pytest.mark.xfail
            ],
            id='incomprehensible_behavior'
        )
    ]
)
def test_login_data_validation(email, password, status_code, api_client):
    endpoint = reverse('login')
    data = {
        'email': email,
        'password': password
    }
    response = api_client.post(endpoint, data=data, format="json")
    assert response.status_code == status_code


@pytest.mark.django_db
def test_login(api_client):
    user = UserFactory(password="my-pass")
    data = {
        'email': user.email,
        'password': "my-pass"
    }
    endpoint = reverse('login')
    response = api_client.post(endpoint, data=data, format="json")
    assert response.status_code == 200
