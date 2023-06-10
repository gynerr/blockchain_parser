import json
import fake_useragent
import requests
from bs4 import BeautifulSoup
import re
from loguru import logger
import csv

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)


def get_data(url: str, start_block: str, end_block: str) -> list:
    result = []
    blocks = range(start_block, end_block + 1)
    for block in blocks:
        block_transactions_url = f'{url}/txs?block={block}'
        logger.info(f'Ожидание ответа от страницы с блоком {block}!')
        response = requests.get(block_transactions_url, headers=headers).text
        response_soup = BeautifulSoup(response, 'lxml')
        pages_count = response_soup.find_all('li', class_='page-item disabled')
        filter_page_counts = \
            str(list(filter(lambda x: x.find('span', class_='page-link text-nowrap'), pages_count))[0])
        pages = list(filter(lambda x: x.isdigit(), filter_page_counts))[-1]
        logger.info(pages)
        for page in range(1, int(pages) + 1):
            logger.info(f'Обработка страницы номер {page}!')
            response = requests.get(f'{block_transactions_url}&p={page}', headers=headers).text
            logger.info(f'{block_transactions_url}&p={page}')
            response_soup = BeautifulSoup(response, 'lxml')
            data = response_soup.find('body').find('table').find_all('tr')
            for i in data[1:]:
                td_div_with_data = i.find_all('td')
                data = td_div_with_data[9].find('div', class_='d-flex d-flex align-items-center gap-1').find('a')[
                    'href']
                adress = re.search(r'/address/(0x[a-fA-F0-9]+)', data)
                result.append(adress.group(1) if adress else 'Адресса в столбце не найдено!!')
    return result


def format_data(data: list) -> list:
    logger.info('Форматирование данных!')
    if config_data['address_format'] == '0x':
        if config_data['remove_doubles'] == True:
            return list(set(data))
        else:
            return data
    elif config_data['address_format'] != '0x':
        data = list(map(lambda x: x.lstrip('0x'), data))
        if config_data['remove_doubles'] == True:
            return list(set(data))
        else:
            return list(data)


def write_data(data: list) -> None:
    logger.info('Вывод')
    if config_data['format_file'] == 'csv':
        with open(
                f'{config_data["blockchain_name"]}_{config_data["file_name"]}_{config_data["start_block"]}-{config_data["end_block"]}.csv',
                'w', newline='\n',
                encoding='Utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(list(map(lambda x: [x], data)))

    elif config_data['format_file'] == 'txt':
        with open(f'{config_data["blockchain_name"]}_{config_data["file_name"]}_{config_data["start_block"]}-{config_data["end_block"]}.txt', 'w',
                  encoding='Utf-8') as file:
            for i in data:
                file.write(i + '\n')


if __name__ == '__main__':
    write_data(format_data(get_data(config_data['url'], config_data['start_block'], config_data['end_block'])))
