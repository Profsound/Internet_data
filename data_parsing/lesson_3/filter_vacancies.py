from pymongo import MongoClient

# Написать функцию, которая производит поиск и
# выводит на экран вакансии с заработной платой больше введенной суммы


client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies = db.hh_table

def find_vac_salary(min_salary, currency='руб'):
    return vacancies.find({'min': {'$gte':min_salary}, 'cur': currency})

#  варианты валют 'руб', 'EUR', 'USD', 'KZT'
vacs = find_vac_salary(2450, 'EUR')

for vac in vacs:
    print(vac)

