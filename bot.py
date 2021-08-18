import telebot
from ansible_collections.dellemc.enterprise_sonic.plugins.module_utils.network.sonic.argspec.users import users

import main
from bot_config import read_bot_config
#from aiogram import types   
#import traceback

bot_config = read_bot_config()
token = bot_config['token']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    id_User = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username

    users = [id_User, first_name, last_name, username]
    
    main.query_users(users)

    bot.send_message(message.chat.id, 'Добро пожаловать 👋, ' + message.chat.first_name)


@bot.message_handler(commands=['tournaments'])
def tour_message(message):
    for tournament in main.all_tournaments():
            bot.send_message(message.chat.id, '🏆 \n' + tournament)
            

@bot.message_handler(commands=['weekend_tournaments'])
def wtour_message(message):
    bot.send_message(message.chat.id, 'Турниры на выходные 👀 ... \n\n' + main.weekend_tournaments())

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Здравствуй!')

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю скажи что-нибудь другое 😕')


if __name__ == '__main__':
    bot.polling()