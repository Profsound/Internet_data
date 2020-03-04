from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from wbparser.spiders.wildberries import WildberriesSpider
from wbparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(WildberriesSpider, mark='ноутбук asus')
    process.start()