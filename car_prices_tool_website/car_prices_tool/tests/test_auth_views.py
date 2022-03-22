import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
