# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from wbparser.items import WBparserItem
from scrapy.loader import ItemLoader


class WildberriesSpider(scrapy.Spider):
    name = 'wildberries'
    allowed_domains = ['wildberries.ru']

    def __init__(self, mark):
        self.start_urls = ["https://www.wildberries.ru/catalog/0/search.aspx?search=%s" %mark]

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="ref_goods_n_p"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=WBparserItem(), response=response)
        loader.add_xpath('name','//div[@class="brand-and-name j-product-title"]//span[2]/text()')
        loader.add_xpath('price','//span[@class="final-cost"]/text()')
        loader.add_xpath('photos','//a[@class="j-photo-link"]/@href')
        yield loader.load_item()