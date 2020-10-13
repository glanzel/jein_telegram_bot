import telebot
from telebot import types

bot = telebot.TeleBot("BOT_TOKEN")

# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# - resize_keyboard: True/False (default False)
# - one_time_keyboard: True/False (default False)
# - selective: True/False (default False)
# - row_width: integer (default 3)
# row_width is used in combination with the add() function.
# It defines how many buttons are fit on each row before continuing on the next row.
markup = types.ReplyKeyboardMarkup(row_width=3)
itembtn1 = types.KeyboardButton('a')
itembtn2 = types.KeyboardButton('v')
itembtn3 = types.KeyboardButton('d')
markup.add(itembtn1, itembtn2, itembtn3)
#bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)

@bot.inline_handler(func=lambda message: True)
def query_text(inline_query):
    bot.reply_to(inline_query, "This is inline mode.")
    print("This is inline mode.")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "This Bot only provides inline mode.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    print("achso?")

bot.polling()
