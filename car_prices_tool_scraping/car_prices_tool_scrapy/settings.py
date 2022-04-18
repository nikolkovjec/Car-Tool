BOT_NAME = 'car_prices_tool_scrapy'

SPIDER_MODULES = ['car_prices_tool_scrapy.spiders']
NEWSPIDER_MODULE = 'car_prices_tool_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5

# between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True

ROTATING_PROXY_LIST_PATH = 'car_prices_tool_scrapy/http_proxies.txt'
USER_AGENT_LIST = 'car_prices_tool_scrapy/user_agents.txt'

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 10
#CONCURRENT_REQUESTS_PER_IP = 16

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'car_prices_tool_scrapy.middlewares.CarPricesToolScrapyDownloaderMiddleware': 543,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'random_useragent.RandomUserAgentMiddleware': 400
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'car_prices_tool_scrapy.pipelines.JsonPipeline': 900,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False
