from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobsdata import settings
from jobsdata.spiders.headhunter import HeadhunterSpider
from jobsdata.spiders.superjob import SuperjobSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # hh_process = CrawlerProcess(settings=crawler_settings)
    # hh_process.crawl(HeadhunterSpider)
    # hh_process.start()

    sj_process = CrawlerProcess(settings=crawler_settings)
    sj_process.crawl(SuperjobSpider)
    sj_process.start()