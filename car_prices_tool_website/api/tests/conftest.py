import pytest

from car_prices_tool.models import UserPremiumRank


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        kwargs['password'] = 'TestPassword'
        if 'username' not in kwargs:
            kwargs['username'] = 'TestUser'
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    UserPremiumRank.objects.create(user=user, rank='APIPRO')
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
