import pytest

from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestViews:
    def test_home_view(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_about_view(self, client):
        url = reverse('about')
        response = client.get(url)
        assert response.status_code == 200

    def test_features_view(self, client):
        url = reverse('features')
        response = client.get(url)
        assert response.status_code == 200

    def test_pricing_view(self, client):
        url = reverse('pricing')
        response = client.get(url)
        assert response.status_code == 200

    def test_sign_up_user_view(self, client):
        url = reverse('signup')
        response = client.get(url)
        assert response.status_code == 200

    def test_log_in_user_view(self, client):
        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200

    def test_load_models_view(self, client):
        url = reverse('ajax_load_models')
        response = client.get(url)
        assert response.status_code == 200

    def test_results(self):
        path = reverse('results')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        context = {
            'make': 'Kia',
            'state': 'Used',
            'model': 'Ceed'
        }

        from car_prices_tool.views import results
        response = results(request, context)
        assert response.status_code == 200

    def test_full_results(self):
        path = reverse('results')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        context = {
            'make': 'Volkswagen',
            'model': 'Golf',
            'state': 'Used',
            'offer_type': 'person',
            'mileage_less_more': 'mileage_more_than',
            'mileage': '70000',
            'production_year_less_more': 'production_year_less_than',
            'production_year': '2012',
            'engine_capacity_less_more': 'engine_capacity_more_than',
            'engine_capacity': '1.0',
            'engine_power_less_more': 'engine_power_more_than',
            'engine_power': '60',
            'price_less_more': 'price_less_than',
            'price': '120000',
            'price_currency': 'pln'
        }

        from car_prices_tool.views import results
        response = results(request, context)
        assert response.status_code == 200

    def test_unauthorized_results(self):
        path = reverse('results')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        context = {
            'make': 'Kia',
            'state': 'Used',
            'model': 'Ceed'
        }

        from car_prices_tool.views import results
        response = results(request, context)
        assert response.status_code == 302

    def test_demo_results(self):
        path = reverse('results_demo')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        context = {
            'make': 'Kia',
            'state': 'Used',
            'model': 'Ceed'
        }

        from car_prices_tool.views import results_demo
        response = results_demo(request, context)
        assert response.status_code == 200
