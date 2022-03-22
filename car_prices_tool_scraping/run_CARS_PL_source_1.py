import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from car_prices_tool_scrapy.spiders.CARS_PL_source_1 import CARSPLsource1Spider


class CARSPLSource1:
    def __init__(self):
        settings_file_path = 'car_prices_tool_scrapy.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = CARSPLsource1Spider

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()
