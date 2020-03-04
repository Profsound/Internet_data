# -*- coding: utf-8 -*-

from jobsdata.items import JobsdataItem
from typing import Dict
import re
from pymongo import MongoClient
from pymongo import errors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class JobsdataPipeline(object):
    def process_item(self, item, spider):
        return item

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['vacanciesDB1']
        self.db["SuperJob"].drop()
        # self.db['HeadHunter'].drop()


    def process_item(self, item: JobsdataItem, spider):
        salary = self.parse_compensation(comp=item['salary'])
        result = {}
        result.update(item)
        del result['salary']
        result.update(salary)
        result['source'] = spider.name

        try:
            self.db[spider.name].insert_one(result)
        except(errors.WriteError, errors.WriteConcernError) as e:
            print('ERROR adding new record %s' % str(result))
            print(e)

        return item

    def parse_compensation(self, comp: str) -> Dict:
        salary_min = salary_max  = currency = ''
        comp_search = re.search('(от)?([0-9 ]+)?(до|-)?([0-9 ]+)? (.*)$', comp.lower().replace('\xa0', ''))
        if comp_search:
            if comp_search.group(2):
                salary_min = int(comp_search.group(2))
            if comp_search.group(3) and '-' in comp_search.group(3) or comp_search.group(
                    3) and 'до' in comp_search.group(3):
                salary_max  = int(comp_search.group(4))
            elif comp_search.group(1) and 'до' in comp_search.group(1):
                salary_max  = int(comp_search.group(2))
            if salary_max or salary_min:
                currency = comp_search.group(5)

        return {'salary_min': salary_min, 'salary_max': salary_max , 'currency': currency}

