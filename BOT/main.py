import requests
import os
from bs4 import BeautifulSoup
from mysql.connector import MySQLConnection
from mysql_dbconfig import read_db_config
from mysql.connector import Error
from datetime import date 
from datetime import timedelta
import tournament
from datetime import datetime   #Библиотеки

def date(): #функция для вывода сегодняшней даты            
    today = datetime.now().date()
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

def insert_tournament(tournaments): #добавляет турниры в базу данных
    for tour in tournaments:
        query = "INSERT INTO tournament_go (t_start, t_end, t_name, city, link) VALUES(%s, %s, %s, %s, %s)"

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, [tour.start, tour.end, tour.name, tour.city, tour.link])
            conn.commit()
        except Error as e:
            print('Error:', e)

        finally:
            cursor.close()
            conn.close()

def insert_tournament20(tournaments20): #добавляет детские турниры в базу данных
    for tour20 in tournaments20:
        query = "INSERT INTO tournaments_up_to_20 (t_start, t_end, t_name, city, link) VALUES(%s, %s, %s, %s, %s)"

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, [tour20.start, tour20.end, tour20.name, tour20.city, tour20.link])
            conn.commit()
        except Error as e:
            print('Error:', e)

        finally:
            cursor.close()
            conn.close()

def main(): #связывает 2 функции insert_tournament и getText
    tournaments = getText()
    insert_tournament(tournaments)

def main20(): #связывает 2 функции insert_tournament20 и getText_up_to_20
    tournaments20 = getText_up_to_20()
    insert_tournament20(tournaments20)

def getText(): #получает текст для вставки новых турниров в базу данных
    html = open('difference.html')
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    tournaments = []

    for t in tr:
        td = t.select('td')
        a = t.select('a')
        tour = tournament.Tournament()

        for i in td:
           
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
                t_name = i.text.replace(" (", ", ").replace(")", "")
                tour.setName(t_name)
                continue

            link = "https://gofederation.ru" + str(a[0].attrs['href'])
            tour.setLink(link)
            
            city = i.text.replace("Сервер", "")
            tour.setCity(city)

        is_children_tournament = False
        if tour.name != "":
            for categories in set_children_categories():
                if categories in tour.name:
                    is_children_tournament = True
                    break
            if not is_children_tournament:
                tournaments.append(tour)

    return tournaments

def getText_up_to_20(): #получает текст для вставки детских новых турниров в базу данных
    html = open('difference.html')
    root = BeautifulSoup(html, 'lxml')
    tr = root.select('tr')
    tournaments20 = []

    for t in tr:
        td = t.select('td')
        a = t.select('a')
        tour20 = tournament.Tournament20()

        for i in td:
           
            if "padding-right" in str(i):
                text_date = i.text.replace("\xa0-\xa0", "")
                format_string = "%d.%m.%Y"
                t_start = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                tour20.setStart(t_start)
                continue

            if "padding-left" in str(i):
                text_date = i.text
                format_string = "%d.%m.%Y"
                t_end = datetime.strptime(text_date, format_string).strftime("%Y-%m-%d")
                tour20.setEnd(t_end)
                continue

            if "tournament" in str(i):
                t_name = i.text.replace(" (", ", ").replace(")", "")
                tour20.setName(t_name)
                continue

            link = "https://gofederation.ru" + str(a[0].attrs['href'])
            tour20.setLink(link)
            
            city = i.text.replace("Сервер", "")
            tour20.setCity(city)

        is_children_tournament = False
        if tour20.name != "":
            for categories in set_children_categories():
                if categories in tour20.name:
                    is_children_tournament = True
                    break
            if is_children_tournament:
                tournaments20.append(tour20)
                is_children_tournament = False

    return tournaments20

def set_children_categories(): #запрос на получение списка категорий

    children_categories = []
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT categories FROM `children_categories`;")
        records = cursor.fetchall()
        for categories in records:
            children_categories.append(categories[0])

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
    return children_categories

def delete_old_tournaments(): #удаляет старые турниры, у которых дата старта меньше тукущей даты
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

def delete_old_tournaments20(): #удаляет старые детские турниры, у которых дата старта меньше тукущей даты
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        date_var = str(date())
        sql = "DELETE FROM tournaments_up_to_20 WHERE DATE(t_start) < DATE(%s);"
        params = [date_var]
        cursor.execute(sql, params)
        conn.commit()
        

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def all_tournaments(): #выполняет запрос на вывод пользователю всех туниров
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city, link FROM tournament_go;")
        all_tournaments = []
        result = cursor.fetchall()
        for item in result:
            tournament = "Начало: " + str(item[0]) + "\n"
            tournament += "Конец: " + str(item[1]) + "\n\n"
            tournament += "Название: " + item[2] + "\n\n"
            tournament += "Город: " + item[3] + "\n\n"
            tournament += "Подробнее: " + item[4] + "\n"
            all_tournaments.append(tournament)
            
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return all_tournaments

def all_tournaments20(): #выполняет запрос на вывод пользователю всех детских туниров
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city, link FROM tournaments_up_to_20;")
        all_tournaments20 = []
        result = cursor.fetchall()
        for item in result:
            tournament = "Начало: " + str(item[0]) + "\n"
            tournament += "Конец: " + str(item[1]) + "\n\n"
            tournament += "Название: " + item[2] + "\n\n"
            tournament += "Город: " + item[3] + "\n\n"
            tournament += "Подробнее: " + item[4] + "\n"
            all_tournaments20.append(tournament)
            
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return all_tournaments20

def all_tournaments_in_city(chatID): #выполняет запрос на вывод пользователю всех туниров в его городе
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city, link FROM tournament_go;")
        all_tournaments = []
        result = cursor.fetchall()

        city_user = my_city(chatID)

        for res in result:
            if res[3] in city_user:
                tournament = "Начало: " + str(res[0]) + "\n"
                tournament += "Конец: " + str(res[1]) + "\n\n"
                tournament += "Название: " + res[2] + "\n\n"
                tournament += "Город: " + res[3] + "\n\n"
                tournament += "Подробнее: " + res[4] + "\n"
                all_tournaments.append(tournament)

        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return all_tournaments

def weekend_tournaments(): #выполняет запрос на вывод пользователю турниров, которые состоятся на выходных текущей недели
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city, link FROM tournament_go;")
        tournament = ""
        result = cursor.fetchall()

        for item in result:
            if item[0] == get_saturday() or item[0] == get_sunday():
                tournament += "Начало: " + str(item[0]) + "\n"
                tournament += "Конец: " + str(item[1]) + "\n\n"
                tournament += "Название: " + item[2] + "\n\n"
                tournament += "Город: " + item[3] + "\n\n"
                tournament += "Подробнее: " + item[4] + "\n\n"
               
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return tournament

def weekend_tournaments20(): #выполняет запрос на вывод пользователю детских турниров, которые состоятся на выходных текущей недели
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT t_start, t_end, t_name, city, link FROM tournaments_up_to_20;")
        tournament20 = ""
        result = cursor.fetchall()

        for item in result:
            if item[0] == get_saturday() or item[0] == get_sunday():
                tournament20 += "Начало: " + str(item[0]) + "\n"
                tournament20 += "Конец: " + str(item[1]) + "\n\n"
                tournament20 += "Название: " + item[2] + "\n\n"
                tournament20 += "Город: " + item[3] + "\n\n"
                tournament20 += "Подробнее: " + item[4] + "\n\n"
               
        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return tournament20

def get_saturday(): #эта функция получает дату субботы текущей недели 
    num_date = datetime.now().date().weekday()
    today = datetime.now().date()
    saturday = ""

    if num_date == 0:
        saturday = today + timedelta(days=5)
    if num_date == 1:
        saturday = today + timedelta(days=4)
    if num_date == 2:
        saturday = today + timedelta(days=3)    
    if num_date == 3:
        saturday = today + timedelta(days=2)
    if num_date == 4:
        saturday = today + timedelta(days=1)
    if num_date == 5:
        saturday = today + timedelta(days=0)
    if num_date == 6:
        saturday = today + timedelta(days=6)

    return saturday

def get_sunday(): #эта функция получает дату воскресенья текущей недели 
    num_date = datetime.now().date().weekday()
    today = datetime.now().date()
    sunday = ""

    if num_date == 0:
        sunday = today + timedelta(days=6)
    if num_date == 1:
        sunday = today + timedelta(days=5)
    if num_date == 2:
        sunday = today + timedelta(days=4)    
    if num_date == 3:
        sunday = today + timedelta(days=3)
    if num_date == 4:
        sunday = today + timedelta(days=2)
    if num_date == 5:
        sunday = today + timedelta(days=1)
    if num_date == 6:
        sunday = today + timedelta(days=0)

    return sunday

def check_exist_user(chatID): #проверка записи пользователя, чтобы не записывался один пользователь несколько раз

    query = "SELECT * FROM `user_BotGo` WHERE id_User='" + str(chatID) + "';"
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query)

        if len(cursor.fetchall()) != 0:
            return True
        else:
            return False

    except Error as e:
        print('Error:', e)

    finally:
        conn.close()

def query_users(users): #выполнение запроса на заполнение данных о пользователе

    if check_exist_user(users[0]):
        return

    query = "INSERT INTO user_BotGo (id_User, first_name, last_name, username, state_user) VALUES( %s, %s, %s, %s, %s)"
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, users)
        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def query_change_state(state, chatID): #запрос на смену состояния пользователя

    query = "UPDATE user_BotGo SET state_user = '" + state + "' WHERE id_User = '" + str(chatID) + "'"
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, state)
        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def add_city(chatID, city): #запрос на добавления пользователю города, в которых он хочет получать информацию о новых турнирах

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO UserCity (id_user, city) VALUES ('" + str(chatID) + "', '" + str(city) + "');")
        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def selectState(chatID): #проверка состояния пользователя

    SelectState = ""
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT state_user FROM user_BotGo WHERE id_User = '" + str(chatID) + "'")
        records = cursor.fetchall()
        SelectState = records[0][0]
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
    return SelectState

def my_city(chatID): ####

    my_city = ""
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT city FROM UserCity WHERE id_user = '" + str(chatID) + "'")
        records = cursor.fetchall()
        my_city = []
        for item in records:
            my_city.append(item[0])
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
    return my_city

def get_all_cities(): #запрос на получение списка городов

    all_city = []
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM `Cities`;")
        records = cursor.fetchall()
        for city in records:
            all_city.append(city[0])

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
    return all_city

def tournaments_in_my_city(chatID):
    tournament_in_my_city = ""
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT city FROM UserCity WHERE id_user = '" + str(chatID) + "'")
        records = cursor.fetchall()
        tournament_in_my_city = records
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
    return tournament_in_my_city

def insert_NEW_tournament(tournaments): #функция записывает новые турниры в таблицу НОВЫЕ турниры го, рассылает, записывает в обычную таблицу, удаляет из новых турниров 
    for tour in tournaments:
        query = "INSERT INTO NEW_tournament_go (t_start, t_end, t_name, city, link) VALUES(%s, %s, %s, %s, %s)"

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(query, [tour.start, tour.end, tour.name, tour.city, tour.link])
            conn.commit()
        except Error as e:
            print('Error:', e)

        finally:
            cursor.close()
            conn.close()

def main_NEW(): #связывает 2 функции insert_NEW_tournament и getText
    tournaments = getText()
    insert_NEW_tournament(tournaments)

def all_cities_from_new_tournaments():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT city FROM NEW_tournament_go")
        result = cursor.fetchall()
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
        return result

def user_cities():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT city FROM UserCity")
        result = cursor.fetchall()
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
        return result

def id_user_where_city_in_NEW():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT id_user FROM UserCity WHERE city in (SELECT city FROM NEW_tournament_go)")
        result = cursor.fetchall()
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
        return result

def all_tournaments_in_city_NEW(chatID): #выполняет запрос на вывод пользователю всех туниров в его городе
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT id, t_start, t_end, t_name, city, link FROM NEW_tournament_go;")
        all_tournaments = []
        result = cursor.fetchall()

        city_user = my_city(chatID)

        for res in result:
            if res[4] in city_user:
                tournament = "Начало: " + str(res[1]) + "\n"
                tournament += "Конец: " + str(res[2]) + "\n\n"
                tournament += "Название: " + res[3] + "\n\n"
                tournament += "Город: " + res[4] + "\n\n"
                tournament += "Подробнее: " + res[5] + "\n"
                all_tournaments.append([res[0], tournament])

        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return all_tournaments

def delete_all_from_NEW():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NEW_tournament_go")
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def message_was_send(userID, tournament):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO message_was_send (id_user, tournament) VALUES ('" + str(userID) + "', '" + str(tournament) + "')")
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def Select_message_was_send(userID, tournament):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT id_user, tournament FROM message_was_send WHERE id_user = '" + str(userID) + "' AND tournament = '" + str(tournament) + "';"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()
        return result

def del_message_was_send():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM message_was_send")
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def remove_city_for_user(userID): 
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM UserCity WHERE id_user=" + str(userID))
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


# if __name__ == '__main__':
    
#         get_sunday()


         