import requests
import time
import os
from bs4 import BeautifulSoup
from itertools import islice


def download_page(url, name):
    r = requests.get(url)
    with open(name, 'w') as output_file:
        output_file.write(r.text)

    r.close()


def compare(old_page, current_page):
    with open(old_page, 'r') as f:
        #old_list = set(f.readlines()) 
        delimiter = ''
        sentenceOld = str(delimiter.join(f))

        #soup = BeautifulSoup(sentenceOld, 'lxml')
        #print(soup.find("table"))

    with (open(current_page, 'r')) as f:
        #current_list = set(f.readlines())
        delimiter = ''
        sentenceCurrent = str(delimiter.join(f))

        #soup = BeautifulSoup(sentenceCurrent, 'lxml')
        #print(soup.find("table"))

    open('difference.html', 'w').close()

    with open('difference.html', 'a') as f:
        diff = str(sentenceCurrent) - str(sentenceOld)
        #for line in list(sentenceCurrent -= sentenceOld):
        f.write(diff)

            #line = sentenceOld.difference(sentenceCurrent)


def copy_current_to_old(old_page, current_page):
    with open(current_page, 'r') as current:
        with open(old_page, 'w') as old:
            old.write(current.read())
            old.close()
            current.close()


def check_exist_file(name):
    if not os.path.isfile(name):
        with open(name, 'w'): pass


if __name__ == '__main__':
    while True:

        check_exist_file("current.html")
        check_exist_file("old.html")

        print("Получаем актуальную информацию о турнирах...")
        download_page("https://gofederation.ru/tournaments/", "current.html")
        print("Актуальная информация о турнирах получена...")


        print("Сравниваем изменения...")
        compare("current.html", "old.html")
        print("Сравнение изменений произведено...")

        print("Запись изменений...")
        check_exist_file("difference.html")
        print("Запись изменений получена...")

        print("Перезапись...")
        copy_current_to_old("old.html", "current.html")
        print("Готово")

        # Приостанавливаем выполнение программы на 10с
        #print("Ожидаем 10с...")
        #time.sleep(10)
