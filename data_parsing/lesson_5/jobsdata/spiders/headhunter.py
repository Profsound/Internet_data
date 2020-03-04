# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobsdata.items import JobsdataItem


class HeadhunterSpider(scrapy.Spider):
    name = 'HeadHunter'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1002&st=searchVacancy&text=angular']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href')
        for vacancy in vacancies:
            yield response.follow(vacancy.extract(), callback=self.job_parse)

    @staticmethod
    def job_parse(resp:HtmlResponse):
        result = dict()
        result['title'] = ''.join(resp.xpath('//div[contains(@class, "vacancy-title")]/h1/span/text()').extract())
        if not result['title']:
            result['title'] = ''.join(resp.xpath('//div[contains(@class, "vacancy-title")]/h1/text()').extract())

        result['salary'] = ''.join(resp.xpath('//p[@class="vacancy-salary"]/text()').extract())
        result['link'] = resp.url
        yield JobsdataItem(result)