from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import time

# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

# Для примера был взят ресурс с адресами магазинов по ссылке https://www.letu.ru/stores
# Адреса добавляются по 4 при клике на "Загрузить еще 4 магазина"

# Данные: адрес, метро, время работы, телефон и добавочные номера

client = MongoClient('localhost', 27017)
mongo_db = client.leturu
store_collection = mongo_db.letu_addresses
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.letu.ru/stores')

time.sleep(3)
while True:
    try:
        next_shops = driver.find_element_by_xpath('//button[@class ="btn btn-default"]')
        next_shops.click()
    except NoSuchElementException:
        break

lists = driver.find_elements_by_xpath('//div[@class ="stores-list-item__inner"]')
all_shops = []
for shop in lists:
    info = dict()
    info['address'] = shop.find_element_by_class_name('stores-list-item__header').text.replace('\n', ' - ')
    description = shop.find_elements_by_class_name('info-list__item')
    attr_len = len(description)

    info['metro'] = '-' if attr_len == 2 else description[0].text
    info['hours'] = description[attr_len-2].text
    phones = description[attr_len-1].text.split(' доб.')
    info['phones'] = phones[0]
    info['additional'] = phones[1].split(', ')
    if store_collection.find(info).count() > 0:
        print('Магазин %s уже есть в списках' %(info['address']))
    else:
        all_shops.append(info)


if all_shops:
    store_collection.insert_many(all_shops)
print('Количество адресов магазинов Л\'Этуаль: %s' % (str(len(all_shops))))











