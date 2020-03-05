from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from pymongo import MongoClient
import time

# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

# Сбор писем работает только при следующих настройках внешнего вида: пункты должны быть отключены
# "Список писем с колонкой письма" и "Группировка по отправителю" должны быть отключены

ACCESS = {
    'login': 'study.ai_172@mail.ru',
    'passw': 'NewPassword172'
}

def sign_in_ok(drv):
    drv.find_element_by_id("mailbox:login").send_keys(ACCESS['login'])
    drv.find_element_by_class_name("o-control").submit()
    elem = WebDriverWait(drv, 3).until(EC.element_to_be_clickable((By.ID, 'mailbox:password')))
    elem.send_keys(ACCESS['passw'])
    elem.send_keys(Keys.ENTER)
    time.sleep(1)
    return drv.title.find('Входящие') > -1


def fill_content_to_db(drv, collection):
    email = drv.find_element_by_xpath('//a[contains(@class,"llc js-tooltip-direction_letter-bottom '
                                      'js-letter-list-item llc_normal")]')
    email.send_keys(Keys.ENTER)
    not_last_email = True
    time.sleep(1)
    while not_last_email:
        content = dict()
        try:
            content['sender'] = drv.find_element_by_class_name('letter-contact').text
            content['datentime'] = drv.find_element_by_class_name('letter__date').text
            content['header'] = drv.find_element_by_class_name('thread__subject').text
            content['message'] = drv.find_element_by_class_name('letter-body__body-content').text
        except StaleElementReferenceException:
            # ждем догрузки страницы и попытаемся снова
            time.sleep(1)
            content['sender'] = drv.find_element_by_class_name('letter-contact').text
            content['datentime'] = drv.find_element_by_class_name('letter__date').text
            content['header'] = drv.find_element_by_class_name('thread__subject').text
            content['message'] = drv.find_element_by_class_name('letter-body__body-content').text
        collection.insert_one(content)
        # if collection.find(content).count() > 0:
        #     print('already exists', content['header'])
        # else:
        #     collection.insert_one(content)

        # next_email = drv.find_element_by_xpath('//span[@title="Следующее"]')
        next_email = drv.find_element_by_xpath(
            '//span[contains(@class,"button2_arrow-down")]')  # '//span[@title="Следующее"]'

        if 'button2_disabled' in next_email.get_attribute('class'):
            # Почему-то отрабатывало на некоторых письмах как последнее.
            # Ждем некоторое время для обновления элементов DOM
            time.sleep(2)
            if 'button2_disabled' in next_email.get_attribute('class'):
                # Должно быть: This is the last email in list -  Как воспользоваться почтой с мобильного?
                print('This is the last email in list - ', content['header'])
                not_last_email = False
            else:
                next_email.click()
        else:
            next_email.click()


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    # убираем отображение фото для быстрой загрузки всей страницы
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=chrome_options)
    # driver.fullscreen_window()
    driver.get('https://mail.ru/')
    assert "Mail.ru: почта" in driver.title

    client = MongoClient('localhost', 27017)
    mongo_db = client.mailru
    mail_collection = mongo_db.mailru_emails

    if sign_in_ok(driver):
        fill_content_to_db(driver, mail_collection)
    else:
        print('O-ops! Something is wrong')
    driver.quit()







