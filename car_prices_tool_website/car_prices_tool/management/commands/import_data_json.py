import json
import random
import pendulum

from django.core.management.base import BaseCommand

from car_prices_tool.models import Car


class Command(BaseCommand):
    """
    This command was written to automate process of importing data from json file to django models.
    Json file is being prepared by Scrapy spider with cars data. Each time this command is called,
    old data is being deleted and new one is being imported. Additional field 'price_dollars' is
    being added to make comparing cars with different price currencies easier.
    You can call this command by writing 'python manage.py import_data_json'.
    """

    mode = 'full'

    def handle(self, **options):
        if not self.mode:
            self.stdout.write(self.style.WARNING('Please provide "mode" as "full" ot "test" to determine how much '
                                                 'data you want to import.'))
            return

        with open('car_prices_tool_django/file.json', 'r') as f:
            cars = json.load(f)

        self.stdout.write('Deleting all CARS models data...')

        # Delete all previous objects
        Car.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted old CARS models data!'))

        self.stdout.write('Creating new CARS models data...')

        # Create a django model object for each object in JSON
        for car in cars:
            if self.mode == 'full':
                self.create_car_object(car)
            elif self.mode == 'test':
                if random.randint(0, 100) == 1:
                    self.create_car_object(car)

        self.stdout.write(self.style.SUCCESS(f'Successfully added new CARS models data in {self.mode} mode!'))

    @staticmethod
    def create_car_object(car):
        if car['price_currency'] != 'USD':
            if car['price_currency'] == 'PLN':
                price_dollars = car['price'] * 0.27
            if car['price_currency'] == 'EUR':
                price_dollars = car['price'] * 1.21
        else:
            price_dollars = car['price']

        Car.objects.create(
            make=car['make'],
            model=car.get('model'),
            model_variant=car.get('model_variant'),
            production_year=car.get('production_year'),
            engine_power=car.get('engine_power'),
            mileage=car.get('mileage'),
            engine_capacity=car.get('engine_capacity'),
            offer_type=car.get('offer_type'),
            price=car['price'],
            price_currency=car.get('price_currency'),
            state=car.get('state'),
            price_dollars=price_dollars,
            date_scraped=pendulum.from_format(car.get('date_scraped'), 'DD/MM/YYYY'),
            date_issued=pendulum.from_format(car.get('date_issued'), 'DD/MM/YYYY')
        )
