from django.contrib.auth.models import User
from django.test import TestCase

from car_prices_tool.models import Car, UserPremiumRank


class TestModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestModels, cls).setUpClass()
        cls.user = User.objects.create_user("TestUser")
        cls.user.set_password("TestPassword")

    def test_example_car(self):
        example_car = Car.objects.create(
            make='TestMake',
            model='TestModel',
            production_year=2017,
            engine_power=190,
            mileage=156000,
            engine_capacity=2.8,
            offer_type='business',
            price=158790,
            price_currency='PLN',
            state='Used',
            date_scraped='2021-02-21',
            date_issued='2021-02-15'
        )

        assert example_car in Car.objects.all()

    def test_create_user(self):
        user = self.user

        assert user.username == "TestUser"
        assert user.check_password("TestPassword")
        assert User.objects.count() == 1

    def test_user_premium_rank(self):
        user = self.user

        premium_rank = UserPremiumRank.objects.create(
            user=user,
            rank='Premium'
        )

        assert premium_rank in UserPremiumRank.objects.all()
