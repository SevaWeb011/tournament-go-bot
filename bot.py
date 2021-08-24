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

        all_city = main.get_all_cities()
        for city in all_city:
            towns.add(types.KeyboardButton(city))
        
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Привет, выбери город 🏘, в котором ты хочешь получать уведомления о турнирах 😉', reply_markup=towns)
            
        if message.html_text in all_city:
            main.add_city(message.chat.id, message.html_text)
            bot.send_message(message.chat.id, 'Если хочешь выбрать еще города, нажми ДАЛЕЕ, если нет, то нажми СТОП', reply_markup=navigation)
            
        if message.html_text == 'далее':
            bot.send_message(message.chat.id, 'Выбери город', reply_markup=towns)

        if message.html_text == 'стоп':
            main.query_change_state("main", message.chat.id)
            bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name, reply_markup=types.ReplyKeyboardRemove())

               


    if SelectState == "main":
        if message.text.lower() == "/start":
            bot.send_message(message.chat.id, 'Здравствуй, ' + message.chat.first_name)

        if message.text.lower() == "/tournaments":
            for tournament in main.all_tournaments():
                bot.send_message(message.chat.id, '🏆 \n' + tournament)

        if message.text.lower() == "город":
            for city in main.all_cities():
                bot.send_message(message.chat.id, city)

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