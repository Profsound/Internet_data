from lxml import html
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver               # для новостей из mail.ru
from selenium.webdriver.common.by import By  # для новостей из mail.ru
import pymorphy2                             # для новостей из lenta.ru (названия месяцев)
import requests
import locale                                # для новостей из lenta.ru (названия месяцев)

# 1)Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# - название источника,
# - наименование новости,
# - ссылку на новость,
# - дата публикации

header = {'User-Agent': 'Chrome/77.0.3865.40'}
path_to_driver = '/mnt/libs/chromedriver'


def get_datetime(pubdate):
    # устанавливаем русскоязычный формат даты и времени
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    dl = [x.strip() for x in pubdate.split(',')]
    m = pymorphy2.MorphAnalyzer()
    day, month, year = dl[1].split(' ')
    # преобразуем название месяца в именительный падеж с заглавной буквы
    new_month = m.parse(month)[0].inflect({'nomn'}).word.title()
    dt_obj = datetime.strptime(' '.join([dl[0], day, new_month, year]), '%H:%M %d %B %Y')
    return dt_obj


def get_dt(urls, titles, resourses):
    # Попытка получить даты и времени публикации,
    # но даты есть на страницах СМИ (у всех разные оформления)
    # for i in range(len(urls)):
    #     print(urls[i], titles[i], resourses[i])
    #     response = requests.get(urls[i])
    #     root = html.fromstring(response.text)

    #     Есть список ниже со временем публикации, но он не всегда содержит
    #     тот же источник с датой и временем (нужно подгружать нажатием кнопки "Показать еще")
    #     resourse_node = root.xpath("//a[text()=titles[i]]")
    #     print(resourse_node)
    return datetime.now()


def get_lenta_news():
    current_news = []
    article = {}
    news_url = 'https://www.lenta.ru'
    response = requests.get(news_url)
    root = html.fromstring(response.text)
    list_of_news = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']")
    for news in list_of_news:
        href = news_url + news.xpath(".//a/@href")[0]
        title = news.xpath(".//a/text()")[0].replace('\xa0', ' ')
        pub_date = get_datetime(news.xpath(".//a/time/@datetime")[0])
        article['href'] = href
        article['media'] = 'Лента.РУ'
        article['title'] = title
        article['published'] = pub_date
        current_news.append(article)
        article = {}
    return current_news


def get_yandex_news():
    current_news = []
    article = {}
    news_url = 'https://www.yandex.ru'
    response = requests.get(news_url, headers=header)
    root = html.fromstring(response.text)
    list_of_news = root.xpath("//div[contains(@class,'news__panel mix-tabber-slide2__panel')]")
    href = list_of_news[0].xpath("./ol/li/a/@href")
    hrefs = [h.split('?')[0] for h in href]
    resourses = list_of_news[0].xpath("./ol/li/a/span/div/object[@class='news__agency-icon-image']/@title")
    titles = list_of_news[0].xpath("./ol/li/a/@aria-label")
    pub_datetime = get_dt(hrefs, titles, resourses)
    for i in range(len(href)):
        article['href'] = hrefs[i]
        article['media'] = resourses[i]
        article['title'] = titles[i]
        article['published'] = pub_datetime
        current_news.append(article)
        article = {}
    return current_news


def get_media_info(url):
    try:
        response = requests.get(url, headers=header)
        root = html.fromstring(response.text)
        media_block = root.xpath("//a[@class='link color_gray breadcrumbs__link']")[0]
        media = media_block.xpath(".//span[@class='link__text']")[0].text
        date_block = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']")[0]
        published = date_block.xpath(".//@datetime")[0][:19]
        return [media, published]
    except:
        return '-'


def get_mail_news():
    current_news = []
    article = {}
    news_url = 'https://www.mail.ru'
    driver = webdriver.Chrome(path_to_driver)
    driver.get(news_url)
    list_of_news = driver.find_elements(By.XPATH, "//div[contains(@class,'news-item svelte-1089u92')]")
    for news in list_of_news[:-3]:
        title = news.text
        href = news.find_element(By.XPATH, ".//a").get_attribute('href')
        media_info = get_media_info(href)
        article['href'] = href
        article['media'] = media_info[0]
        article['published'] = datetime.strptime(media_info[1], '%Y-%m-%dT%H:%M:%S')
        article['title'] = title
        current_news.append(article)
        article = {}
    driver.quit()
    return current_news


def fill_news_db():
    client = MongoClient('localhost', 27017)
    db = client['news_db']
    news_collection = db.news

    ln = get_lenta_news()
    print("Новости из Лента.ру: " + str(len(ln)))
    news_collection.insert_many(ln)

    yan = get_yandex_news()
    print("Новости из Яндекс: " + str(len(yan)))
    news_collection.insert_many(yan)

    mail = get_mail_news()
    print("Новости из Mail.ru: " + str(len(mail)))
    news_collection.insert_many(mail)


if __name__ == "__main__":
    fill_news_db()
