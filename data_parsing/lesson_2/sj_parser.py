from bs4 import BeautifulSoup as bs
import requests as req
import re

def get_salary(salary):
    # salary = 'По договорённости'
    # salary = '110 000 — 120 000 ₽'
    # salary = 'от 130 000 ₽'
    currency_dict = {
        "₽": 'руб',
        "$": 'USD',
        "€": 'EUR'
    }
    result = {'min': 0, 'max': 0, 'cur': 'руб'}
    if not salary == 'По договорённости':
        salary = salary.replace('\xa0—\xa0', '-').replace('\xa0', ' ')
        salary_min = salary_max = currency = ''
        comp_search = re.search('(от)?([0-9 ]+)?(до|-)?([0-9 ]+)? (.*)$', salary.lower())
        if comp_search:
            if comp_search.group(2):
                salary_min = int(comp_search.group(2).replace(' ', ''))
            if comp_search.group(3) and '-' in comp_search.group(3) or comp_search.group(3) and 'до' in comp_search.group(3):
                salary_max = int(comp_search.group(4).replace(' ', ''))
            elif comp_search.group(1) and 'до' in comp_search.group(1):
                salary_max = int(comp_search.group(2).replace(' ', ''))
            if salary_max or salary_min:
                currency = comp_search.group(5)
        result['cur'] = currency_dict[currency]
        result['min'] = salary_min
        result['max'] = salary_max
    return result


def get_vacancies(search_text):
    hostname = 'https://www.superjob.ru'
    final_data = []
    get_page = hostname + '/vacancy/search/?geo%5Bt%5D%5B0%5D=4'
    headers = {
        'user-agent': 'Mozilla/5.0'
    }
    params = {
        'keywords': search_text
    }
    while get_page:
        response = req.get(get_page, headers=headers, params=params).text
        html = bs(response, 'lxml')
        list_of_vacancies = html.find_all(attrs={"class": "_3syPg _3P0J7 _9_FPy"})

        for vacancy in list_of_vacancies:
            temp_data = {}
            salary_comp = {'min': 0, 'max': 0, 'cur': ''}
            salary_info = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).text
            if salary_info:
                salary_comp = get_salary(salary_info)
            title_info = vacancy.select('a[class*="f-test-link-"]')[0]

            temp_data['name'] = title_info.getText()
            temp_data['url'] = hostname + title_info['href']
            temp_data['web'] = hostname
            temp_data['min'] = salary_comp['min']
            temp_data['max'] = salary_comp['max']
            temp_data['cur'] = salary_comp['cur']
            final_data.append(temp_data)
        next_url = html.find('a', {'class': 'f-test-button-dalshe'})
        get_page = hostname + next_url.get('href') if next_url else False
    return final_data



if __name__ == "__main__":
    # print(get_salary('По договорённости'))
    # print(get_salary('110 000 — 120 000 $'))
    # print(get_salary('от 130 000 ₽'))
    # print(get_salary('до 10 000 €'))
    print(get_vacancies('devops'))
