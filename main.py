import json
import fake_useragent
import requests
from bs4 import BeautifulSoup
import re
from loguru import logger
import csv
import os

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}



with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

if config_data['format_file'] == 'csv':
    config_data['line_count'] = 1048576

def format_data(data: list) -> list:
    logger.info('Форматирование данных!')
    if config_data['address_format'] == '0x':
        if config_data['remove_doubles'] == True:
            return list(set(data))
        else:
            return data
    elif config_data['address_format'] != '0x':
        data = list(map(lambda x: x[2:], data))
        if config_data['remove_doubles'] == True:
            return list(set(data))
        else:
            return list(data)


def write_data(data: list) -> None:
    logger.info('Вывод')
    if not os.path.exists(config_data['folder_name']):
        os.makedirs(config_data['folder_name'])
    if config_data['format_file'] == 'csv':
        with open(
                f'{config_data["folder_name"]}/{config_data["blockchain_name"]}_{config_data["file_name"]}_{config_data["start_block"]}-{config_data["end_block"]}.csv',
                'a', newline='\n',
                encoding='Utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(list(map(lambda x: [x], data)))
    elif config_data['format_file'] == 'txt':
        with open(os.path.join(config_data['folder_name'], f'{config_data["blockchain_name"]}_{config_data["file_name"]}_{config_data["start_block"]}-{config_data["end_block"]}.txt'), 'a',
                  encoding='Utf-8') as file:
            for i in data:
                file.write(i + '\n')

def get_data(url: str, start_block: str, end_block: str) -> list:
    blocks = range(start_block, end_block + 1)
    count_string = 0
    for block in blocks:
        result = []
        block_transactions_url = f'{url}/txs?block={block}'
        logger.info(f'Ожидание ответа от страницы с блоком {block}!')
        response = requests.get(block_transactions_url, headers=headers).text
        response_soup = BeautifulSoup(response, 'lxml')
        pages_count = response_soup.find_all('li', class_='page-item disabled')
        filter_page_counts = \
            list(filter(lambda x: x.find('span', class_='page-link text-nowrap'), pages_count))
        if filter_page_counts:
            pages = list(filter(lambda x: x.isdigit(), str(filter_page_counts[0])))[-1]
            for page in range(1, int(pages) + 1):
                logger.info(f'Обработка страницы номер {page}!')
                response = requests.get(f'{block_transactions_url}&p={page}', headers=headers).text
                response_soup = BeautifulSoup(response, 'lxml')
                data = response_soup.find('body').find('table').find_all('tr')
                for i in data[1:]:
                    td_div_with_data = i.find_all('td')
                    data = td_div_with_data[-4].find('a')['href']
                    adress = re.search(r'/address/(0x[a-fA-F0-9]+)', data)
                    result.append(adress.group(1) if adress else 'Адресса в столбце не найдено!!')
        else:
            data_table = response_soup.find('body').find('table')
            if data_table:
                data = data_table.find_all('tr')
                for i in data[1:]:
                    td_div_with_data = i.find_all('td')
                    if len(td_div_with_data) > 1:
                        data = td_div_with_data[-4].find('a')['href']
                        adress = re.search(r'/address/(0x[a-fA-F0-9]+)', data)
                        result.append(adress.group(1) if adress else 'Адресса в столбце не найдено!!')
            else:
                logger.warning('Таблица не найдена в HTML-разметке из-за проблем с сетью!')
        count_string += len(result)
        if count_string > config_data['line_count']:
            logger.warning('Кол-во строк превышает параметр line_count в конфигурационном файле!')
            break
        else:
            write_data(format_data(result))



if __name__ == '__main__':
    get_data(config_data['url'], config_data['start_block'], config_data['end_block'])
