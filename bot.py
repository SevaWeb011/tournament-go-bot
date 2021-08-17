import telebot
import main
from bot_config import read_bot_config

bot_config = read_bot_config()
token = bot_config['token']
bot = telebot.TeleBot(token)

#def on_start(update, context):
	#chat = update.effective_chat
	#context.bot.send_message(chat_id=chat.id, text="Привет, я бот")

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Все турниры', 'Турниры на ближайших выходных')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

#@bot.message_handler(commands=['tournaments'])
#def start_message(message):
    #markup = telebot.types.InlineKeyboardMarkup()
    #markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
    #markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
    #markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
    #bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'все турниры':
        for tournament in main.all_tournaments():
            bot.send_message(message.chat.id, tournament)

    elif message.text.lower() == 'турниры на ближайших выходных':
        bot.send_message(message.chat.id, main.weekend_tournaments())
        #str.split([разделитель [, maxsplit]])


if __name__ == '__main__':
    bot.polling()