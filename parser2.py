import random
from typing import List, Callable

import bs4.element
import requests
from bs4 import BeautifulSoup as Bs


def clear_text(text: str):
    return text.replace('\n', '').strip()


def try_get(func) -> Callable[[bs4.element.Tag], str]:
    def wrapper(article: bs4.element.Tag, *args, **kwargs) -> str:
        try:
            return func(article, *args, **kwargs)
        except AttributeError:
            return ''
    return wrapper


def get_html(url_to_get: str) -> str:
    return requests.get(url_to_get).text


def get_news(html: str) -> List[dict]:
    soup = Bs(html, 'lxml')

    @try_get
    def get_title(article: bs4.element.Tag) -> str:
        return clear_text(article.find(class_='ArticleItem--name').text)

    @try_get
    def get_img(article: bs4.element.Tag) -> str:
        return clear_text(article.find('img').attrs.get('src'))

    @try_get
    def get_link(article: bs4.element.Tag) -> str:
        return clear_text(article.find('a', class_='ArticleItem--name').attrs.get('href'))

    return [{'title': get_title(item), 'image': get_img(item), 'link': get_link(item)} for item in soup.find_all(class_='ArticleItem', limit=20)]


def get_description(html: str):
    soup = Bs(html, 'lxml')
    return '\n'.join([p.text for p in soup.find(class_='Article--text').find_all('p')])


if __name__ == '__main__':
    import datetime
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    url = f'https://kaktus.media/?lable=8&date={today}&order=time'
    news = get_news(get_html(url))
    print(get_description(get_html(news[0]['link'])))

