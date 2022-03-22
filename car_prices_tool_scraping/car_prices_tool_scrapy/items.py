import re

import scrapy
from itemloaders.processors import Join, MapCompose


def clean_item(item):
    if item:
        item = re.sub(r'\s+', ' ', str(item)).strip()
        return item


def remove_spaces(item):
    if item:
        item = str(item).replace(' ', '')
        return item


def convert_to_int(item):
    if item:
        item = int(float(str(item).replace(',', '.')))
        return item


def convert_to_float(item):
    if item:
        item = float(item)
        return item


class Car(scrapy.Item):
    # Simple string like Opel or Audi
    make = scrapy.Field(
        input_processor=MapCompose(clean_item),
        output_processor=Join()
    )
    # Simple string like Zafira or A1
    model = scrapy.Field(
        input_processor=MapCompose(clean_item),
        output_processor=Join()
    )
    # String like 1.4 TFSI Sportback S tronic or S Line Competion S Tronic 5dr (need to somehow simplfy it)
    model_variant = scrapy.Field(
        input_processor=MapCompose(clean_item),
        output_processor=Join()
    )
    # Simple int like 1999 or 2007
    production_year = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        serializer=convert_to_int,
        output_processor=Join()
    )
    # Simple int like 96 or 245
    engine_power = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        serializer=convert_to_int,
        output_processor=Join()
    )
    # Simple int like 164000 or 72000
    mileage = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        serializer=convert_to_int,
        output_processor=Join()
    )
    # Simple float like 1.6 or 2.4
    engine_capacity = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        serializer=convert_to_float,
        output_processor=Join()
    )
    # Simple string person or business
    offer_type = scrapy.Field(
        input_processor=MapCompose(clean_item),
        output_processor=Join()
    )
    # Simple string like 120000 or 12000
    price = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        serializer=convert_to_int,
        output_processor=Join()
    )
    # Simple string like PLN or EUR
    price_currency = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        output_processor=Join()
    )
    # Simple string Used or New
    state = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        output_processor=Join()
    )
    # Date in a string format 'DD/MM/YYYY'
    date_issued = scrapy.Field(
        input_processor=MapCompose(clean_item, remove_spaces),
        output_processor=Join()
    )
    # Standard pendulum now string
    date_scraped = scrapy.Field(
        output_processor=Join()
    )
    # Check if car is not damaged (if damaged is True pipeline will drop item)
    damaged = scrapy.Field()
