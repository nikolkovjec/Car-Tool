import inspect
import json
import os
import re
import sys

import pendulum
from scrapy import spiders
from scrapy.loader import ItemLoader

# This will make sure that we won't encounter any import errors (both locally and with docker)
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from items import Car


class CARSPLsource1Spider(spiders.CrawlSpider):
    name = "CARS_PL_source_1"
    # 'source_1' is a temp name for website url that is being scraped
    start_urls = ['https://www.source_1.pl']

    def parse_start_url(self, response):
        data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        makes = data['props']['pageProps']['filtersValues']['571'][1]['group_values']

        # For loop to scrape used cars.
        for make in makes[:1]:
            url = response.urljoin(f'/osobowe/uzywane/{make["search_key"]}/')

            yield response.follow(url, callback=self.parse_cars)

        # For loop to scrape new cars.
        for make in makes[:1]:
            url = response.urljoin(f'/osobowe/nowe/{make["search_key"]}/')

            yield response.follow(url, callback=self.parse_cars)

    def parse_cars(self, response):
        cars = response.xpath('//article/div[2]/div/h2/a/@href').getall()

        for car in cars:
            yield response.follow(car, callback=self.parse_car_detail)

        next_page = response.xpath('//ul[@class="om-pager rel"]/li[@class="next abs"]/a/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse_cars)

    def parse_car_detail(self, response):
        make = response.xpath('//*[contains(text(), "Marka pojazdu")]/following::*[1]/a/text()').get()

        model = response.xpath('//*[contains(text(), "Model pojazdu")]/following::*[1]/a/text()').get('')
        if 'Inny' in model:
            model = 'Other'

        model_variant = response.xpath('//*[contains(text(), "Wersja")]/following::*[1]/a/text()').get()
        production_year = response.xpath('//*[contains(text(), "Rok produkcji")]/following::*[1]/text()').get()
        engine_power = response.xpath('//*[contains(text(), "Moc")]/following::*[1]/text()').re_first(r'(.+) KM')

        mileage = response.xpath('//*[contains(text(), "Przebieg")]/following::*[1]/text()').re_first(r'(.+) km')
        if mileage:
            mileage = int(mileage.replace(' ', ''))

        engine_capacity = response.xpath('//*[contains(text(), "Pojemność skokowa")]/following::*[1]/text()').re_first(r'(.+) cm3')
        # Get format of engine_capacity as float 1.9 or 2.3
        if engine_capacity:
            engine_capacity = f'{float(int(engine_capacity.replace(" ", "")) / 1000):.1f}'

        offer_type = response.xpath('//*[contains(text(), "Oferta od")]/following::*[1]/a/text()').get()
        if 'Osoby prywatnej' in offer_type:
            offer_type = 'person'
        elif 'Firmy' in offer_type:
            offer_type = 'business'

        price = response.xpath('//div[@class="offer-price changeFinanceLinkOrder"]/span/text()').get()
        price_currency = response.xpath('//div[@class="offer-price changeFinanceLinkOrder"]/span/span/text()').get()

        state = response.xpath('//*[contains(text(), "Stan")]/following::*[1]/a/text()').get('')
        if 'Używane' in state:
            state = 'Used'
        elif 'Nowe' in state:
            state = 'New'

        damaged = bool(response.xpath('//*[contains(text(), "Uszkodzony")]/following::*[1]/a/text()').get())

        date_issued = response.xpath('//span[@class="offer-meta__value"]/text()').re_first(r', (.+)')
        day = re.findall(r'(^\d+)|$', date_issued)[0]
        month = self.get_month(date_issued)
        year = re.findall(r'(\d{4})|$', date_issued)[0]
        date_issued = f'{day}/{month}/{year}'

        # Item loader
        car = ItemLoader(item=Car(), selector=response)
        car.add_value('make', make)
        car.add_value('model', model)
        car.add_value('model_variant', model_variant)
        car.add_value('production_year', production_year)
        car.add_value('engine_power', engine_power)
        car.add_value('mileage', mileage)
        car.add_value('engine_capacity', engine_capacity)
        car.add_value('offer_type', offer_type)
        car.add_value('price', price)
        car.add_value('price_currency', price_currency)
        car.add_value('state', state)
        car.add_value('date_scraped', pendulum.now('CET').format('DD/MM/YYYY'))
        car.add_value('date_issued', date_issued)
        car.add_value('damaged', damaged)

        return car.load_item()

    @staticmethod
    def get_month(date_issued):
        month = re.findall(r'[a-zA-Zęóąśłżźćń]+|$', date_issued)[0]
        if 'stycz' in month:
            month = '01'
        elif 'lut' in month:
            month = '02'
        elif 'mar' in month:
            month = '03'
        elif 'kwie' in month:
            month = '04'
        elif 'maj' in month:
            month = '05'
        elif 'czerw' in month:
            month = '06'
        elif 'lip' in month:
            month = '07'
        elif 'sierp' in month:
            month = '08'
        elif 'wrze' in month:
            month = '09'
        elif 'październik' in month:
            month = '10'
        elif 'listopad' in month:
            month = '11'
        elif 'grud' in month:
            month = '12'

        return month
