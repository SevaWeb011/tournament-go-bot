import requests
import os
from bs4 import BeautifulSoup
from mysql.connector import MySQLConnection
from mysql_dbconfig import read_db_config
from mysql.connector import Error
from datetime import date
import datetime as DT
from datetime import datetime   #Библиотеки

def data():          #функция для вывода сегодняшней даты            
    today=datetime.now()
    wd=date.weekday(today)
    days= ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    print(today)
    print("which is a " + days[wd])

def download_page(url, name):  #функция для скачивания актуальной версии турниров по ссылке
    r = requests.get(url)
    with open(name, 'w') as output_file:
        output_file.write(r.text) 
    r.close()


def record_set(page): #функция, которая удаляет все переносы строк в файле (делает одну строку)
    with open(page, 'r') as f:
        content = f.read().replace('\n', '')
        soup = BeautifulSoup(content, 'lxml')
        result_set = set()
        for item in soup.find_all("tr"):
            result_set.add(str(item))
        return result_set         


def compare(current_page, old_page): #функция для сравнения старой версии турниров с новой, различия записываются в файл difference
    old_records = record_set(old_page)
    current_records = record_set(current_page)
    open('difference.html', 'w').close()
    new_records = []

    with open('difference.html', 'a') as f: # проверка отличий
        for line in current_records:
            if line not in old_records:
                new_records.append(line)
        f.writelines(new_records)

def copy_current_to_old(old_page, current_page): # функция для перезаписи старой версии файла
    with open(current_page, 'r') as current:
        with open(old_page, 'w') as old:
            old.write(current.read())
            old.close()
            current.close()


def check_exist_file(name):
    if not os.path.isfile(name):
        with open(name, 'w'): pass

def connect():
    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')

    except Error as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')


def query():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tournament_go")
        print(cursor.execute)
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def insert_tournament(tournament):
    html = open('current.html')
    open('tournament.html', 'w').close()
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    with open('tournament.html', 'w') as f: 

        for t in tr:
            td = t.select('td')
            for i in td:
                print(i.text)
                if 'class="m"' in str(i):
                    f.writelines(i.text.replace(i.text, ""))
                    continue

                if "padding-right" in str(i):
                    f.writelines(i.text.replace(" - ", "") + "\n")
                    continue

                if "padding-left" in str(i):
                    f.writelines(i.text + "\n")
                    continue

                if "tournament" in str(i):
                    f.writelines(i.text + "\n")
                    continue

                f.writelines(i.text + "\n\n")
    query = "INSERT INTO tournament_go (t_start, t_end, t_name, city) VALUES(%s, %s, %s, %s)"

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.executemany(query, tournament)
        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def main():
    tournament = [({t_start}, {t_end}, {t_name}, {city})]
    insert_tournament(tournament)

def getText(): 
    html = open('current.html')
    #open('tournament.html', 'w').close()
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    with open('tournament.html', 'w') as f: 

        for t in tr:
            td = t.select('td')
            for i in td:
                print(i.text)
                if 'class="m"' in str(i):
                    f.writelines(i.text.replace(i.text, ""))
                    continue

                if "padding-right" in str(i):
                    f.writelines(i.text.replace(" - ", "") + "\n")
                    text_date = i.text.replace("\xa0-\xa0", "")
                    format_string = "%d.%m.%Y"
                    t_start = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                    continue

                if "padding-left" in str(i):
                    f.writelines(i.text + "\n")
                    text_date = i.text
                    format_string = "%d.%m.%Y"
                    t_end = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                    continue

                if "tournament" in str(i):
                    f.writelines(i.text + "\n")
                    t_name = i.text
                    continue

                f.writelines(i.text + "\n\n")
                city = i.text
            
        

if __name__ == '__main__':

        #getText()
        
        #print("Подключение к бд...")
        #connect()
        #print("Ок..")
        
        #print("Получение результата запроса...")
        #main()
        #print("Ок..")

        #print("Получаем актуальную информацию о турнирах...")
        #download_page("https://gofederation.ru/tournaments/", "current.html")
        #print("Актуальная информация о турнирах получена...")

        getText()

        #print("Сравниваем изменения...")
        #compare("current.html", "old.html")
        #print("Сравнение изменений произведено...")

        #print("Запись изменений...")
        #check_exist_file("difference.html")
        #print("Запись изменений получена...")

        #print("Перезапись...")
        #copy_current_to_old("old.html", "current.html")
        #print("Готово")

        #print("Сегодня") 
        #data()