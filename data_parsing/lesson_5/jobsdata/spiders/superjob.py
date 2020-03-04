# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobsdata.items import JobsdataItem
import re


class SuperjobSpider(scrapy.Spider):
    name = 'SuperJob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies = response.xpath('//a[contains(@class, "_2JivQ _3dPok")]/@href')

        for vacancy in vacancies:
            yield response.follow('https://www.superjob.ru' + vacancy.extract(), callback=self.job_parse)

    @staticmethod
    def job_parse(resp:HtmlResponse):
        result = dict()
        result['title'] = ''.join(resp.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]//text()').extract())
        salary = ''.join(resp.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]//text()').extract())
        salary = salary.replace('\xa0—\xa0', '-')
        result['salary'] = re.sub(r'(\d+)\xa0(\d+)', r'\1\2', salary).replace('\xa0', ' ')
        result['link'] = resp.url
        yield JobsdataItem(result)