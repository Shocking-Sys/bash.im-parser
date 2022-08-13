import datetime
import requests

from bs4 import NavigableString

from parser.const import HEADERS, RETRY_ATTEMPTS
import sys, errno


def get_url(page_number):
    return 'https://web.archive.org/bash.im/index/{}'.format(page_number)


def fetch_page(Session, page_number):
    for attempt in range(RETRY_ATTEMPTS):
        try:
            req = Session.get(url=get_url(page_number), headers=HEADERS, timeout=(5, 30))
            try:
                text = req.content.decode('utf-8')
                #print(req.request.headers)
                break
            except Exception as err:
                print('От сайта пришел плохой контент:', err)
        except ConnectionError as err:
            print('Проблема с соеденением:', err)

        if attempt > RETRY_ATTEMPTS-1:
            sys.stderr.write(f'{RETRY_ATTEMPTS}, неудачных попыток спарсить данные, ошибка на странице: {page_number = }\n')
            sys.exit(errno.ECANCELED)

    return text


def parse_quote(quote_article):
    quote = {}

    text_div = quote_article.find('div', class_='quote__body')

    quote['text'] = '\n'.join(
        i.strip() for i in text_div.contents
        if isinstance(i, NavigableString) and i != '\n'
    )

    quote['id'] = quote_article.find(
        'a',
        class_='quote__header_permalink'
    ).string[1:]

    quote['datetime'] = quote_article.find(
        'div',
        class_='quote__header_date'
    ).string.strip()

    return quote


def get_timestamp(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, '%d.%m.%Y в %H:%M')
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()
