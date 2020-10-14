from pyrogram import Client, filters 
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from pyrogram.types.inline_mode.inline_query import InlineQuery


app = Client("my_account")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


from sqlalchemy import func
from base import Session, Base
from reactions import Reactions

buttonstext = ['\U0001F44D', '\U0001F44E', '\U0001F914', '\U00002795']


@app.on_message(filters.private)
async def hello(client, message):
    print(app.get_me())
    await message.reply_text(f"Hello {message.from_user.mention}")

def createButtons():
    buttons = [        [InlineKeyboardButton("\U0001F44D", callback_data="0"),
        InlineKeyboardButton("\U0001F44E", callback_data="1"),
        InlineKeyboardButton("\U0001F914", callback_data="2"),
        InlineKeyboardButton("\U00002795", callback_data="3"),
        InlineKeyboardButton("#", callback_data="99")]                        
    ]
    return buttons

@app.on_inline_query()
async def inline(client, inlineQuery):
    query = inlineQuery.query
    the_reply_markup = InlineKeyboardMarkup(createButtons())
    resultArticle = InlineQueryResultArticle(
        title="post with ja nein buttons",
        input_message_content=InputTextMessageContent(message_text=query),
        reply_markup=the_reply_markup)
    
    results = [resultArticle]

    await inlineQuery.answer(results)

def getUsername(user):
    if user.username is not None:
        return user.username
    elif user.first_name is not None:
        return user.first_name
    else: return user.id
        


@app.on_callback_query()    
def button(client, callbackQuery):
    """Show new choice of buttons"""
    query = callbackQuery
    query.answer()

    #reply_markup = query.message.reply_markup
    button_no = int(query.data)
    username = getUsername(query.from_user)
    print(query.inline_message_id)
    print(query.id)
    print(query.__dict__)

    session = Session()
    
    #save reaction
    if button_no < 98:
        your_reactions = session.query(Reactions).filter(Reactions.message_id == query.inline_message_id, Reactions.user == username).all()
        print(your_reactions)
        if not your_reactions:
            reaction = Reactions(message_id=query.inline_message_id, value=button_no, user=username)
            session.add(reaction)
        else:
            for yr in your_reactions:
                if int(yr.value) == int(button_no): 
                    session.delete(yr)
                else: 
                    yr.value = button_no
                    #session.add(yr)
        session.commit()
        session.close()

    cb_buttons = createButtons()

    #read reactions
    select = session.query(Reactions.value, func.count(Reactions.value)).filter(Reactions.message_id== query.inline_message_id).group_by(Reactions.value).all()
    
    if select:
        for tup in select:
            button_number = int(tup[0])
            button_count = str(tup[1])
            cb_buttons[0][button_number] = InlineKeyboardButton(buttonstext[button_number] + " + " + button_count, callback_data= str(button_number))

    if button_no == 99:
        if 1 not in cb_buttons:
            cb_buttons.append([None]) 
            selectVotes = session.query(Reactions).filter(Reactions.message_id== query.inline_message_id).all()
            print("selectVotes")
            print(selectVotes)
            ergStr = ""
            for reaction in selectVotes:
                ergStr += str(reaction.user)+ " : " + buttonstext[int(reaction.value)]
            cb_buttons[1][0] = InlineKeyboardButton(ergStr, callback_data="98")
        else: del cb_buttons[1]

    
    if button_no == 98:
        if 1 in cb_buttons:
            del cb_buttons[1]

    client.edit_inline_reply_markup(
    query.inline_message_id,
    InlineKeyboardMarkup(cb_buttons))

app.run()



