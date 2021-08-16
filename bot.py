import main
from telebot import apihelper
import telebot
bot = telebot.TeleBot('1977406104:AAEWaArJA8UlIzgrfiY7U-DS0yPmMaQs7fQ')

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Все турниры', 'Пока')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

@bot.message_handler(commands=['tournaments'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
    bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'все турниры':
        bot.send_message(message.chat.id, main.all_tournaments())
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')



bot.polling()