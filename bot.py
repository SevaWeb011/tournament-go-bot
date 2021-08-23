import telebot
from telebot import types
import main
from bot_config import read_bot_config

bot_config = read_bot_config()
token = bot_config['token']
bot = telebot.TeleBot(token)
state = "city_selection"

@bot.message_handler(content_types=['text'])
def message(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    group1 = types.KeyboardButton("Москва, Моск.обл., Жуковский, Тула, Калуга, Калужская обл.")
    group2 = types.KeyboardButton("Санкт-Петербург, Всеволожск, Великий Новгород, Тверь")
    group3 = types.KeyboardButton("Казань")
    group7 = types.KeyboardButton("Нижний Новгород")
    group20 = types.KeyboardButton("Барнаул, Бийск")
    group12 = types.KeyboardButton("Владивосток")
    group6 = types.KeyboardButton("Екатеринбург")
    group8 = types.KeyboardButton("Ижевск")
    group15 = types.KeyboardButton("Калининград")
    group21 = types.KeyboardButton("Краснодар, Анапа, Сочи")
    group14 = types.KeyboardButton("Магадан")
    group17 = types.KeyboardButton("Нижний Тагил")
    group22 = types.KeyboardButton("Николаевск-на-Амуре")
    group18 = types.KeyboardButton("Новосибирск")
    group19 = types.KeyboardButton("Омск")
    group13 = types.KeyboardButton("Пермь")
    group4 = types.KeyboardButton("Петрозаводск")
    group25 = types.KeyboardButton("Ростов-на-Дону")
    group23 = types.KeyboardButton("Тверь")
    group9 = types.KeyboardButton("Тольятти, Самара")
    group11 = types.KeyboardButton("Тюмень")
    group16 = types.KeyboardButton("Хабаровск")
    group10 = types.KeyboardButton("Челябинск")
    group24 = types.KeyboardButton("Якутск")
    
    markup.add(group1)
    markup.add(group2)
    markup.add(group3, group7)
    markup.add(group20, group12)
    markup.add(group6, group8)
    markup.add(group15, group21)
    markup.add(group14, group17)
    markup.add(group22, group18)
    markup.add(group19, group13)
    markup.add(group4, group25)
    markup.add(group23, group9)
    markup.add(group11, group16)
    markup.add(group10, group24)

    id_User = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username
    city = ""
    state_user = "city_selection"

    users = [id_User, first_name, last_name, username, city, state_user]
    main.query_users(users)
  

    SelectState = main.selectState(message.chat.id)

    if SelectState == "city_selection":
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Привет, выбери город 🏘 или группу городов, в котором ты живешь. Если твоего города нет 😔, выбери того, что ближе всего. Я буду уведомлять тебя о новых турнирах 😉', reply_markup = markup)

        if message.html_text == 'Москва, Моск.обл., Жуковский, Тула, Калуга, Калужская обл.':
            city = 'Москва, Моск.обл., Жуковский, Тула, Калуга, Калужская обл.'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())
    
        if message.html_text == 'Санкт-Петербург, Всеволожск, Великий Новгород, Тверь':
            city = 'Санкт-Петербург, Всеволожск, Великий Новгород, Тверь'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())
                  
        if message.html_text == 'Казань':
            city = 'Казань'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())    

        if message.html_text == 'Нижний Новгород':
            city = 'Нижний Новгород'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Барнаул, Бийск':
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Владивосток':
            city = 'Владивосток'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Екатеринбург':
            city = 'Екатеринбург'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Ижевск':
            city = 'Ижевск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Калининград':
            city = 'Калининград'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Краснодар, Анапа, Сочи':
            city = 'Краснодар, Анапа, Сочи'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Магадан':
            city = 'Магадан'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Нижний Тагил':
            city = 'Нижний Тагил'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Николаевск-на-Амуре':
            city = 'Николаевск-на-Амуре'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Новосибирск':
            city = 'Новосибирск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Омск':
            city = 'Омск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Тверь':
            city = 'Тверь'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Пермь':
            city = 'Пермь'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Петрозаводск':
            city = 'Петрозаводск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Ростов-на-Дону':
            city = 'Ростов-на-Дону'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Тюмень':
            city = 'Тюмень'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Хабаровск':
            city = 'Хабаровск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Челябинск':
            city = 'Челябинск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

        if message.html_text == 'Якутск':
            city = 'Якутск'
            main.query_change_city(city, message.chat.id)
            state = "main"
            main.query_change_state(state, message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())
    
    if SelectState == "main":
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Здравствуй, ' + message.chat.first_name)

        if message.text.lower() == "/tournaments":
            for tournament in main.all_tournaments():
                bot.send_message(message.chat.id, '🏆 \n' + tournament)

        if message.text.lower() == "/weekend_tournaments":
            bot.send_message(message.chat.id, 'Турниры на выходные 👀 ... \n\n' + main.weekend_tournaments())

        if message.text.lower() == "/my_city":
            bot.send_message(message.chat.id, 'Твой город:  ' + main.my_city(message.chat.id))

        # if message.text.lower() == "/tournaments_in_my_city":
        #     myCity = main.my_city(message.chat.id))
        #     bot.send_message(message.chat.id, 'Турниры твоего города: ' + main.tournaments_in_my_city(message.chat.id, myCity))

        # state = "main"
        #     main.query_change_state(state, message.chat.id)

if __name__ == '__main__':
    bot.polling()