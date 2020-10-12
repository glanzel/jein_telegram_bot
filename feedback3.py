#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, InlineQueryHandler
import logging
from collections import defaultdict

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

buttons = {0:"yes",1:"no",2:"err",3:"like"}
keyboardButtons = defaultdict(list)


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    buttons = [
        [InlineKeyboardButton("yes", callback_data=0),
         InlineKeyboardButton("no", callback_data=1),
         InlineKeyboardButton("err", callback_data=2),
         InlineKeyboardButton("like", callback_data=3)]
    ]
    the_reply_markup = InlineKeyboardMarkup(buttons)
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Post with buttons",
            input_message_content=InputTextMessageContent(message_text=query, parse_mode=ParseMode.MARKDOWN, description="desc",reply_markup=the_reply_markup))]
    update.inline_query.answer(results)


def bot_article(update, context):
    txt= update.inline_query.query
    buttons = [
        [InlineKeyboardButton("yes", callback_data=0),
         InlineKeyboardButton("no", callback_data=1),
         InlineKeyboardButton("err", callback_data=2),
         InlineKeyboardButton("like", callback_data=3)]
    ]    
    reply_markup = InlineKeyboardMarkup(buttons)
    results = [InlineQueryResultArticle(
        id=uuid4(),
        title="Post with buttons",
        input_message_content=InputTextMessageContent(message_text=txt,
                                                      parse_mode=ParseMode.MARKDOWN),
        description="desc",
        reply_markup=reply_markup
        # thumb_url='http://www.colorcombos.com/images/colors/FF0000.png'
    )]
    update.inline_query.answer(results) 

def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    
#    print(keyboard)
    for k, v in buttons.items():
        keyboardButtons[k] = InlineKeyboardButton(v, callback_data=k)
            
    keyboard = [
        [InlineKeyboardButton("yes", callback_data=0),
         InlineKeyboardButton("no", callback_data=1),
         InlineKeyboardButton("err", callback_data=2),
         InlineKeyboardButton("like", callback_data=3)]
    ]

    #keyboard = [keyboardButtons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Start handler, Choose a route",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST



def button(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    reply_markup = query.message.reply_markup
    button_no = int(query.data)
    #print(context.chat_data[button_no])
    username = query.message.chat.username
    if button_no not in  context.chat_data.keys():  context.chat_data[button_no] = {"votes":dict(),"text":buttons[button_no]}
    btn = context.chat_data[button_no]
    if username in  btn["votes"].keys():
         del btn["votes"][username]
    else:
        btn["votes"][username] = 1
    
    reply_markup.inline_keyboard[0][button_no].text = btn["text"] +" +"+ str(len(btn["votes"])) 

    query.edit_message_text(
		text=query.message.text,
        reply_markup=reply_markup
    )
    print(query.message)
    print("__________lalalalala_________________")
    print(query.data)
    
    return FIRST


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("1384153335:AAHdPY1IeGbtvjYzl_U6aIdOg_oPYoXoFE8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    #dp.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    #updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(InlineQueryHandler(bot_article))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
