from pymongo import MongoClient
from lesson_two import hh_parser

# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies = db.hh_table


def parse_and_fill(vacname, code):
    # Пример для вакансии devops
    # 1 - код для Москвы
    # 2 - Санкт-Петербург
    # 1624 - Татарстан

    data_to_db = hh_parser.get_vacancies(vacname, code)
    print('Найдено %s вакансий по запросу: %s' %(len(data_to_db)), vacname)
    vacancies.insert_many(data_to_db)

# Распарсим и зальем данные в БД mongo
parse_and_fill('java прогаммист', 1624)