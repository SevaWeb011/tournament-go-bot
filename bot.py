import telebot
import main
from bot_config import read_bot_config

bot_config = read_bot_config()
token = bot_config['token']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! 👋')

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