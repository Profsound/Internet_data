from bs4 import BeautifulSoup as bs
import requests as req
import re


def get_salary(salary):
    # salary = '10 000-300 000 руб.'
    # salary = 'до 3000 USD'
    # salary = 'от 300 000 руб.'
    result = {'min': 0, 'max': 0, 'cur': 'руб'}
    salary = salary.replace('\xa0', ' ').replace('.', '')
    result['cur'] = salary.split(' ')[-1]
    match1 = re.search(r'^[0-9 ]+-[0-9 ]+', salary)
    if match1:
        s = match1[0].replace(' ', '').split('-')
        u = [int(x.replace(' ', '')) for x in s]
        result['min'] = u[0]
        result['max'] = u[1]
    match2 = re.search(r'^до [0-9 ]+ \w+$', salary)
    if match2:
        s = re.split('[a-яА-Яa-zA-Z]+', salary)
        u = list(filter(None, s))
        u = [int(x.replace(' ', '')) for x in u]
        result['max'] = u[0]
    match3 = re.search(r'^от [0-9 ]+ \w+$', salary)
    if match3:
        s = re.split('[a-яА-Яa-zA-Z]+', salary)
        u = list(filter(None, s))
        u = [int(x.replace(' ', '')) for x in u]
        result['min'] = u[0]
    return result


def get_vacancies(search_text, area=1):
    final_data = []
    get_page = 'https://hh.ru/search/vacancy'
    headers = {
        'user-agent': 'Mozilla/5.0'
    }
    params = {
        'L_save_area': 'true',
        'clusters': 'true',
        'enable_snippets': 'true',
        'area': area,
        'text': search_text
    }
    while get_page:
        response = req.get(get_page, headers=headers, params=params).text
        html = bs(response, 'lxml')
        list_of_vacancies = html.find_all(attrs={"class": "vacancy-serp-item"})

        for vacancy in list_of_vacancies:
            temp_data = {}
            salary_comp = {'min': 0, 'max': 0, 'cur': ''}
            salary_info = vacancy.find('div', {'class': 'vacancy-serp-item__compensation'})
            if salary_info:
                salary_comp = get_salary(salary_info.getText())
            title_info = vacancy.find('div', {'class': 'resume-search-item__name'}).findChild()
            vac_name = title_info.getText().replace(',', ';')
            vac_link = title_info.find('a', {'class': 'bloko-link'})['href']

            temp_data['name'] = vac_name
            temp_data['url'] = vac_link
            temp_data['web'] = 'hh.ru'
            temp_data['min'] = salary_comp['min']
            temp_data['max'] = salary_comp['max']
            temp_data['cur'] = salary_comp['cur']
            final_data.append(temp_data)

        next_url = html.find('a', {'class': 'HH-Pager-Controls-Next'})
        get_page ='https://hh.ru' + next_url.get('href') if next_url else False
    return final_data



if __name__ == "__main__":
    # Пример для вакансии devops
    # 1 - код для Москвы
    # 2 - Санкт-Петербург
    # 1624 - Татарстан
    print(get_vacancies('devops', 1624))