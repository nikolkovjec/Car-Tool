from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50, null=True)
    model_variant = models.CharField(max_length=100, null=True)
    production_year = models.IntegerField(null=True)
    engine_power = models.IntegerField(null=True)
    mileage = models.IntegerField(null=True)
    engine_capacity = models.FloatField(null=True)
    offer_type = models.CharField(max_length=10, null=True)
    price = models.IntegerField()
    price_currency = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=10, null=True)
    price_dollars = models.IntegerField(null=True)
    date_scraped = models.DateField(null=True)
    date_issued = models.DateField(null=True)

    def __str__(self):
        return self.make


class UserSearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    search_parameters = JSONField()


class UserPremiumRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50)

    def __str__(self):
        return self.rank
