import pytest


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        kwargs['password'] = 'TestPassword'
        if 'username' not in kwargs:
            kwargs['username'] = 'TestUser'
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username='TestUser', password='TestPassword')
        return client, user

    return make_auto_login


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
