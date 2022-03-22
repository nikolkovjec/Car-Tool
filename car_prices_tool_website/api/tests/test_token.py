import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_authorized_request(api_client_with_credentials):
    url = reverse('api_results')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
