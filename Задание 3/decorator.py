import functools
import bs4
import requests
import json
from datetime import datetime

def logger(old_function):
    @functools.wraps(old_function)
    def new_function(*args, **kwargs):
        with open('data.json', 'w', encoding='utf-8') as data_json:
            func_name = f'Данные получены путем вызова функции - {old_function.__name__!r}'
            time = datetime.now()
            current_time = time.time().strftime('%H:%M')
            current_date = time.date().strftime('%d.%m.%y')
            func_time = current_time
            func_date = current_date

            div = old_function(*args, **kwargs)
            for i in div:
                if 'django' in i.find('a').text.lower() or 'flask' in i.find('a').text.lower():
                    city = i.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
                    href = i.find('a').get('href')
                    name = i.find('a').text
                    salary = i.find('span', class_='bloko-header-section-2')
                    company_name = i.find('div', class_='bloko-text').text
                    if salary is not None:
                        salary = i.find('span', class_='bloko-header-section-2').text
                        salary_str = str(salary)
                        json_data = {
                            'Название функции': func_name,
                            'Дата': current_date,
                            'Время': current_time,
                            'link': href,
                            'vacancy_name': name,
                            'salary': salary_str,
                            'company_name': company_name,
                            'city': city
                        }
                        result = json.dumps(json_data, ensure_ascii=False, indent=4)
                        data_json.write(result)
        return div
    return new_function


url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=3'
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'YandexBrowser',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}


@logger
def url_responce(arg_1, arg_2):
    responce = requests.get(url, headers=headers)
    html_data = responce.text
    soup = bs4.BeautifulSoup(html_data, features='lxml')
    div_tag = soup.find_all('div', class_='serp-item')
    return div_tag

url_responce(url, headers)