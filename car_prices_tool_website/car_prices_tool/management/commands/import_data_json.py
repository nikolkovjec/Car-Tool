import json
from car_prices_tool.models import Car, CarMake
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        with open('car_prices_tool_django/file.json', 'r', encoding='utf-8') as f:
            cars = json.load(f)

        self.stdout.write('Deleting all CARS models data...')

        # Delete all previous objects
        Car.objects.all().delete()
        CarMake.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted old CARS and CARMAKE models data!'))

        self.stdout.write('Creating new CARS and CARMAKE models data...')

        car_makes_list = []

        # Create a django model object for each object in JSON
        for car in cars:
            if car['make'] not in car_makes_list:
                car_makes_list.append(car['make'])
                CarMake.objects.create(car_make=car['make'])

            if car['price_currency'] != 'USD':
                if car['price_currency'] == 'PLN':
                    price_dollars = car['price'] * 0.27
                if car['price_currency'] == 'EUR':
                    price_dollars = car['price'] * 1.21
            else:
                price_dollars = car['price']

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
                price_dollars=price_dollars
                # date_scraped=car['date_scraped']
            )

        self.stdout.write(self.style.SUCCESS('Successfully added new CARS and CAR_MAKE models data!'))
