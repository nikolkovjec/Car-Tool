import os
import sys
import json
import inspect
import pendulum
from scrapy import spiders
# from car_prices_tool_scrapy.items import Car
from scrapy.loader import ItemLoader

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from items import Car


class CARSPLsource1Spider(spiders.CrawlSpider):
    name = "CARS_PL_source_1"
    start_urls = ['https://www.source1.pl']

    def parse_start_url(self, response):
        data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        makes = data['props']['pageProps']['filtersValues']['571'][1]['group_values']
        for make in makes[:1]:
            make = make['search_key']
            url = f'https://www.source1.pl/osobowe/uzywane/{make}/'
            yield response.follow(url, callback=self.parse_cars)

    def parse_cars(self, response):
        cars = response.xpath('//article/div[2]/div/h2/a/@href').getall()

        for car in cars:
            yield response.follow(car, callback=self.parse_car_detail)

        next_page = response.xpath('//ul[@class="om-pager rel"]/li[@class="next abs"]/a/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse_cars)

    def parse_car_detail(self, response):
        make = response.xpath('//*[contains(text(), "Marka pojazdu")]/following::*[1]/a/text()').get('')
        model = response.xpath('//*[contains(text(), "Model pojazdu")]/following::*[1]/a/text()').get('')
        if model == 'Inny':
            model = ''
        model_variant = response.xpath('//*[contains(text(), "Wersja")]/following::*[1]/a/text()').get('')
        production_year = response.xpath('//*[contains(text(), "Rok produkcji")]/following::*[1]/text()').get('')
        engine_power = response.xpath('//*[contains(text(), "Moc")]/following::*[1]/text()').re_first(r'(.+) KM')
        mileage = response.xpath('//*[contains(text(), "Przebieg")]/following::*[1]/text()').re_first(r'(.+) km')
        mileage = int(mileage.replace(' ', ''))
        engine_capacity = response.xpath('//*[contains(text(), "Pojemność skokowa")]/following::*[1]/text()').re_first(r'(.+) cm3')
        # Get format of engine_capacity as float 1.9 or 2.3
        if engine_capacity:
            engine_capacity = '%.1f' % float(int(engine_capacity.replace(' ', ''))/1000)
        offer_type = response.xpath('//*[contains(text(), "Oferta od")]/following::*[1]/a/text()').get('')
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
        damaged = response.xpath('//*[contains(text(), "Uszkodzony")]/following::*[1]/a/text()').get()
        if damaged:
            damaged = 'True'

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
        car.add_value('date_scraped', pendulum.now('CET'))

        if not damaged:
            return car.load_item()
