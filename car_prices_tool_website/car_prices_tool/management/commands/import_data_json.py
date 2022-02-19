import json
from car_prices_tool.models import Car
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        with open('car_prices_tool_django/file.json', 'r', encoding='utf-8') as f:
            cars = json.load(f)

        self.stdout.write('Deleting all CARS models data...')

        # Delete all previous objects
        Car.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted old CARS models data!'))

        self.stdout.write('Creating new CARS models data...')

        # Create a django model object for each object in JSON
        for car in cars:
            Car.objects.create(
                make=car['make'],
                model=car['model'],
                model_variant=car['model_variant'],
                production_year=car['production_year'],
                engine_power=car['engine_power'],
                mileage=car['mileage'],
                engine_capacity=car['engine_capacity'],
                offer_type=car['offer_type'],
                price=car['price'],
                price_currency=car['price_currency'],
                state=car['state'],
                # date_scraped=car['date_scraped']
            )

        self.stdout.write(self.style.SUCCESS('Successfully added new CARS models data!'))
