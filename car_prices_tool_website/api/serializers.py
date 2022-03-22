from rest_framework import serializers
from car_prices_tool.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['make', 'model', 'model_variant', 'production_year', 'engine_power', 'mileage', 'engine_capacity',
                  'offer_type', 'price', 'price_currency', 'state', 'price_dollars', 'date_scraped', 'date_issued']
