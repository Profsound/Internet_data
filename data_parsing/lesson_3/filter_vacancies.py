from pymongo import MongoClient

# Написать функцию, которая производит поиск и
# выводит на экран вакансии с заработной платой больше введенной суммы


client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies = db.vac_table

def find_vac_salary(min_salary, currency='руб'):
    return vacancies.find({'min': {'$gte':min_salary}, 'cur': currency})

#  варианты валют 'руб', 'EUR', 'USD', 'KZT'
vacs = find_vac_salary(100000, 'руб')

for vac in vacs:
    print(vac)

# Пример
# {'_id': ObjectId('5e56308e23e3958975e720f4'), 'name': 'QA Automation Engineer (middle/senior)', 'url': 'https://hh.ru/vacancy/35719238', 'web': 'https://www.hh.ru', 'min': 100000, 'max': 0, 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e720fd'), 'name': 'Руководитель направления разработки', 'url': 'https://hh.ru/vacancy/33942863', 'web': 'https://www.hh.ru', 'min': 205000, 'max': 285000, 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e7210a'), 'name': 'Разработчик Node.Js', 'url': 'https://hh.ru/vacancy/35564302', 'web': 'https://www.hh.ru', 'min': 100000, 'max': 0, 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e72111'), 'name': 'Ведущий разработчик Python', 'url': 'https://www.superjob.ru/vakansii/veduschij-razrabotchik-python-33556879.html', 'web': 'https://www.superjob.ru', 'min': 150000, 'max': 300000, 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e72112'), 'name': 'Программист-разработчик Python', 'url': 'https://www.superjob.ru/vakansii/programmist-razrabotchik-python-33542220.html', 'web': 'https://www.superjob.ru', 'min': 150000, 'max': '', 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e72113'), 'name': 'Разработчик Python, PostgreSQL', 'url': 'https://www.superjob.ru/vakansii/razrabotchik-python-33532143.html', 'web': 'https://www.superjob.ru', 'min': 150000, 'max': '', 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e72117'), 'name': 'Программист', 'url': 'https://www.superjob.ru/vakansii/programmist-33437653.html', 'web': 'https://www.superjob.ru', 'min': 150000, 'max': '', 'cur': 'руб'}
# {'_id': ObjectId('5e56308e23e3958975e72119'), 'name': 'Web-аналитик', 'url': 'https://www.superjob.ru/vakansii/web-analitik-33473129.html', 'web': 'https://www.superjob.ru', 'min': 120000, 'max': 150000, 'cur': 'руб'}