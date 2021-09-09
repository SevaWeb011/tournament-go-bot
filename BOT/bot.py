import os
import time
import threading
from threading import Thread
import telebot
from telebot import types
import main


token = os.getenv("BOT")
bot = telebot.TeleBot(token)
state = "city_selection"
global listCity
listCity = []

@bot.message_handler(content_types=['text'])
def message(message):

    towns = types.ReplyKeyboardMarkup(resize_keyboard=True)

    navigation = types.ReplyKeyboardMarkup(resize_keyboard=True)
    nav1 = types.KeyboardButton('далее')
    nav2 = types.KeyboardButton('стоп')
    navigation.add(nav1, nav2)

    state_user = "city_selection"

    users = [
        message.chat.id,
        message.chat.first_name,
        message.chat.last_name,
        message.chat.username,
        state_user
    ]

    main.query_users(users)

    SelectState = main.selectState(message.chat.id)

    if SelectState == "city_selection":

        all_city = sorted(set(main.get_all_cities()) - set(listCity))
        for city in all_city:
            towns.add(types.KeyboardButton(city))

        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Привет, выбери города 🏘, в которых турниры актуальны для тебя 😉', reply_markup=towns)

        if message.html_text in all_city:
            main.add_city(message.chat.id, message.html_text)
            listCity.append(message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП', reply_markup=navigation)

        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)
       
        if message.html_text == 'стоп':
            main.query_change_state("main", message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())
       

    if SelectState == "main":
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Здравствуй, ' + message.chat.first_name)
            return
       
        if message.text.lower() == "/tournaments":
            for tournament in main.all_tournaments():
                bot.send_message(message.chat.id, '🏆 \n' + tournament)
            return
        
        if message.text.lower() == "/weekend_tournaments":
            bot.send_message(message.chat.id, 'Турниры на выходные 👀 ... \n\n' + main.weekend_tournaments())
            return

        if message.text.lower() == "/my_city":
            for city in main.my_city(message.chat.id):
                bot.send_message(message.chat.id, city)
            return
        
        if message.text.lower() == "/tournaments_in_my_city":
           for tournament in main.all_tournaments_in_city(message.chat.id):
                bot.send_message(message.chat.id, '🏆 \n' + tournament)
           return

        if message.text.lower() == "/message_to_developer":
            main.query_change_state("message_to_developer", message.chat.id)
            SelectState = main.selectState(message.chat.id)
            bot.send_message(message.chat.id, 'Напиши разработчику об ошибках, неисправностях, и тп. Отправь сюда сообщение, чтобы я отправил его разработчику')
            return

        if message.text.lower() == "/change_city":
            main.remove_city_for_user(message.chat.id)
            main.query_change_state("city_selection", message.chat.id)
            SelectState = main.selectState(message.chat.id)
            bot.send_message(message.chat.id, 'Я очистил твои города, выбирай новые', reply_markup=towns)
            return

        else: 
            bot.send_message(message.chat.id, 'Я тебя не понимаю, напиши что-нибудь другое :(')
        
    if SelectState == "message_to_developer" and message.text.lower() != "/message_to_developer":
        bot.send_message(925936432, "Сообщение от " + message.chat.first_name + " " +  message.chat.username + "\n" + message.html_text)
        bot.send_message(message.chat.id, "Отправил")
        main.query_change_state("main", message.chat.id)
        bot.send_message(message.chat.id, 'Если хочешь еще раз написать разработчику, напиши команду /message_to_developer')

def push_message():
    # если выборка city из таблицы NEW_tournament_go 
# есть (in) в выборке города из таблицы UserCity 
# то выполнить запрос к таблице UserCity 
# (выбрать id_user где city = city из таблицы NEW_tournament_go) 
# отправить этому id сообщение о турнире
    for city in main.all_cities_from_new_tournaments():
        if city in main.user_cities():
            for user in main.id_user_where_city_in_NEW():
                all_tournaments = main.all_tournaments_in_city_NEW(user[0])
                for tournament in all_tournaments:
                    result = main.Select_message_was_send(user[0], tournament[0])
                    if len(result) == 0:
                        bot.send_message(user[0], "В твоем городе появился турнир \n" + tournament[1])
                        main.message_was_send(user[0], tournament[0])

def background():#test
    while True:
        main.download_page("https://gofederation.ru/tournaments/", "current.html"),  # скачивание актуальной версии терниров
        main.compare("current.html", "old.html"),  # сравнение
        main.copy_current_to_old("old.html", "current.html"),  # замена старого на новое
        main.main_NEW(),  # запись новых турниров
        push_message(),  # уведомление пользователей о новых турнирах
        main.delete_all_from_NEW(),  # удаление турниров из новых
        main.del_message_was_send(),  # очистка отправленных сообщений
        main.main(),  # добавление новых турниров в основную таблицу
        main.delete_old_tournaments()  # удаление устаревших по дате турниров из основной таблицы

        time.sleep(60)
    

if __name__ == '__main__':

    t1 = Thread(target=background, args=())
    t1.start()
    
    bot.polling()