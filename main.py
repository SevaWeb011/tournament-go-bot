import requests
import os
from bs4 import BeautifulSoup
from mysql.connector import MySQLConnection
from mysql_dbconfig import read_db_config
from mysql.connector import Error
from datetime import date 
from datetime import datetime, timedelta
import tournament
from datetime import datetime   #Библиотеки

def date(): #функция для вывода сегодняшней даты            
    today = datetime.now().date()
    #today = datetime.today().strftime('%Y-%m-%d')
    #print(today)
    return today

def download_page(url, name):  #функция для скачивания актуальной версии турниров по ссылке
    r = requests.get(url)
    with open(name, 'w') as output_file:
        output_file.write(r.text.replace("&nbsp;-&nbsp;", "")) 
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


def insert_tournament(tournaments):
    for tour in tournaments:
        query = "INSERT INTO tournament_go (t_start, t_end, t_name, city) VALUES(%s, %s, %s, %s)"

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, [tour.start, tour.end, tour.name, tour.city])
            conn.commit()
        except Error as e:
            print('Error:', e)

        finally:
            cursor.close()
            conn.close()

def main():
    tournaments = getText()
    insert_tournament(tournaments)

def getText(): 
    html = open('difference.html')
    #open('tournament.html', 'w').close()
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    tournaments = []
    #with open('tournament.html', 'w') as f: 

    for t in tr:
        td = t.select('td')
        tour = tournament.Tournament()

        for i in td:
            if 'class="m"' in str(i):
                continue

            if "padding-right" in str(i):
                text_date = i.text.replace("\xa0-\xa0", "")
                format_string = "%d.%m.%Y"
                t_start = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                tour.setStart(t_start)
                continue

            if "padding-left" in str(i):
                text_date = i.text
                format_string = "%d.%m.%Y"
                t_end = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                tour.setEnd(t_end)
                continue

            if "tournament" in str(i):
                t_name = i.text
                tour.setName(t_name)
                continue

            city = i.text
            tour.setCity(city)

        if tour.name != "":
            tournaments.append(tour)

    return tournaments

def delete_old_tournaments():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        date_var = str(date())
        sql = "DELETE FROM tournament_go WHERE DATE(t_start) < DATE(%s);"
        params = [date_var]
        cursor.execute(sql, params)
        conn.commit()
        

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def all_tournaments():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city FROM tournament_go;")
        all_tournaments = []
        result = cursor.fetchall()
        for item in result:
            tournament = "Начало: " + str(item[0]) + "\n"
            tournament += "Конец: " + str(item[1]) + "\n"
            tournament += "Название: " + item[2] + "\n"
            tournament += "Город: " + item[3] + "\n"
            all_tournaments.append(tournament)
            
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return all_tournaments

def weekend_tournaments():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city FROM tournament_go;")
        tournament = ""
        result = cursor.fetchall()

        for item in result:
            if item[0] == get_saturday():
                tournament += "Начало: " + str(item[0]) + "\n"
                tournament += "Конец: " + str(item[1]) + "\n"
                tournament += "Название: " + item[2] + "\n"
                tournament += "Город: " + item[3] + "\n"
                tournament += "==============================" + "\n\n"
                if item[0] != get_saturday():
                    tournament += "На ближайших выходных турниров нет :("

        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return tournament

def get_saturday():
    num_date = datetime.now().date().weekday()
    today = datetime.now().date()
    saturday = ""

    if num_date == 0 :
        saturday = today + timedelta(days=5)
    if num_date == 1 :
        saturday = today + timedelta(days=4)
    if num_date == 3 :
        saturday = today + timedelta(days=3)
    if num_date == 4 :
        saturday = today + timedelta(days=2)
    if num_date == 5 :
        saturday = today + timedelta(days=1)
    if num_date == 6 :
        saturday = today + timedelta(days=6)

    return saturday


#if __name__ == '__main__':

    
        #print("Получаем актуальную информацию о турнирах...")
        #download_page("https://gofederation.ru/tournaments/", "current.html")
        #print("Актуальная информация о турнирах получена...")

        #print("Сравниваем изменения...")
        #compare("current.html", "old.html")
        #print("Сравнение изменений произведено...")

        #print("Запись изменений...")
        #check_exist_file("difference.html")
        #print("Запись изменений получена...")

        #print("Перезапись...")
        #copy_current_to_old("old.html", "current.html")
        #print("Готово")

        #print("Получение результата запроса...")
        #main()
        #print("Ок..")

        #weekend_tournaments()
        #delete_old_tournaments()

         