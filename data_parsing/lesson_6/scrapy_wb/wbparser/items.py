# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def photo_urls(values):
    if values[:2] == '//':
        return "http:%s" %values
    return


def del_symbols(name_str):
    return ''.join(name_str.replace('\xa0', '').strip())


class WBparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(photo_urls))
    price = scrapy.Field(input_processor=MapCompose(del_symbols))
