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


def record_set(page):
    with open(page, 'r') as f:
        content = f.read().replace('\n', '')
        soup = BeautifulSoup(content, 'lxml')
        result_set = set()
        for item in soup.find_all("tr"):
            result_set.add(str(item))
        return result_set         


def compare(current_page, old_page):
    old_records = record_set(old_page)
    current_records = record_set(current_page)
    open('difference.html', 'w').close()
    new_records = []

    with open('difference.html', 'a') as f:
        for line in current_records:
            if line not in old_records:
                new_records.append(line)
        f.writelines(new_records)

#def copy_current_to_old(old_page, current_page):
    #with open(current_page, 'r') as current:
        #with open(old_page, 'w') as old:
            #old.write(current.read())
            #old.close()
            #current.close()


#def check_exist_file(name):
    #if not os.path.isfile(name):
        #with open(name, 'w'): pass


if __name__ == '__main__':


        #check_exist_file("current.html")
        #check_exist_file("old.html")

        print("Получаем актуальную информацию о турнирах...")
        download_page("https://gofederation.ru/tournaments/", "current.html")
        print("Актуальная информация о турнирах получена...")

        

       # print("Строка старый файл...")
        #record_set("old.html")
        
        print("Сравниваем изменения...")
        compare("current.html", "old.html")
        print("Сравнение изменений произведено...")

       # print("Запись изменений...")
        #check_exist_file("difference.html")
        #print("Запись изменений получена...")

        #print("Перезапись...")
        #copy_current_to_old("old.html", "current.html")
        print("Готово")

        # Приостанавливаем выполнение программы на 10с
        #print("Ожидаем 100с...")
        #time.sleep(100)
