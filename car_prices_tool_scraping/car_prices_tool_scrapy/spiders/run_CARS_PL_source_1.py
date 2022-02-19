from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from CARS_PL_source_1 import CARSPLsource1Spider

process = CrawlerProcess(get_project_settings())
process.crawl(CARSPLsource1Spider)
process.start()
