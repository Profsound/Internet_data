from pymongo import MongoClient
from lesson_2 import hh_parser, sj_parser

# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies = db.vac_table


def parse_and_fill(vacname, code):
    # Пример для вакансии devops
    # 1 - код для Москвы
    # 2 - Санкт-Петербург
    # 1624 - Татарстан

    hh_data_to_db = hh_parser.get_vacancies(vacname, code)
    sj_data_to_db = sj_parser.get_vacancies(vacname)
    print('На HeadHunter найдено %s вакансий по запросу: %s' %(len(hh_data_to_db), vacname))
    print('На SuperJob   найдено %s вакансий по запросу: %s' %(len(sj_data_to_db), vacname))
    vacancies.insert_many(hh_data_to_db)
    vacancies.insert_many(sj_data_to_db)

# Распарсим и заполним данными БД mongo
parse_and_fill('devops', 1624)
# Пример
# На HeadHunter найдено 155 вакансий по запросу: python
# На SuperJob   найдено 32 вакансий по запросу: python