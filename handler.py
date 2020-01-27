from bs4 import BeautifulSoup
import requests
from telegram import send_message
import db

# Функция для получения списка нововстей
def get_html(html, one = False, tag = '', selector={}):
    soup = BeautifulSoup(html, 'html.parser')

    if one:
        list = soup
    else:
        list = soup.findAll(tag,selector)

    return list

# Получение html одной нововсти из списка
def get_html_item_news(html):
    if len(html['href']):
        url = 'https://sport24.ru{}'.format(html['href'])
        if not db.check_url(html['href']):
            db.add_url(html['href'])
            r = requests.get(url)
            r.encoding = 'utf-8'
            html = get_html(r.text, True)

            return  html

#
def get_item_news(html_code):

        html = get_html_item_news(html_code)

        if html is not None:
            return False

        header = html.h1.text

        words = ''

        text = html.find(class_='js-mediator-article _1YOxdQ').find_all('span')

        for t in text:
            if t.find_parent('a'):
                t.extract()
            else:
                text_clean = clean_text(t.get_text())
                words = words + '\t'+text_clean+'\n'

        send_message(words, header)


#Очистка текста от лишних элементов
def clean_text(text):
    text = text.replace("«", '')
    text = text.replace("»", '')
    return text


def test_html(html):
    f = open('test.html', 'w')
    f.write(html)
    f.close()

#Функция для фильтрации данных
def is_good_news(text):
    stop_word = ['жена', 'жену', 'развод', 'Уткин', 'Путин']
    if len(list(filter(lambda x: x in text, stop_word))) > 0:
        return False
    else:
        return True
