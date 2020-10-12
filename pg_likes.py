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

buttonstext = ['yes', 'no', 'err', 'meToo']
buttons = [        [InlineKeyboardButton("yes", callback_data="0"),
     InlineKeyboardButton("no", callback_data="1"),
     InlineKeyboardButton("err", callback_data="2"),
     InlineKeyboardButton("meToo", callback_data="3")]
]


@app.on_message(filters.private)
async def hello(client, message):
    print(app.get_me())
    await message.reply_text(f"Hello {message.from_user.mention}")

def createButtons(message_id):
    buttons[message_id] = [[InlineKeyboardButton("yes", callback_data="0"),
        InlineKeyboardButton("no", callback_data="1"),
        InlineKeyboardButton("err", callback_data="2"),
        InlineKeyboardButton("meToo", callback_data="3"),]
    ]
    return buttons

@app.on_inline_query()
async def inline(client, inlineQuery):
    query = inlineQuery.query
    print(buttons)
    the_reply_markup = InlineKeyboardMarkup(buttons)
    resultArticle = InlineQueryResultArticle(
        title="post with ja nein buttons",
        input_message_content=InputTextMessageContent(message_text=query),
        reply_markup=the_reply_markup)
    
    results = [resultArticle]

    await inlineQuery.answer(results)

@app.on_callback_query()    
def button(client, callbackQuery):
    """Show new choice of buttons"""
    query = callbackQuery
    query.answer()

    #reply_markup = query.message.reply_markup
    button_no = int(query.data)
    username = query.from_user.username
    print(query.inline_message_id)
    print(query.id)
    print(query.__dict__)
    
    #save reaction
    session = Session()
    your_reactions = session.query(Reactions).filter(Reactions.message_id == query.inline_message_id, Reactions.user == username, Reactions.value == button_no).all()
    print(your_reactions)
    if not your_reactions:
        reaction = Reactions(message_id=query.inline_message_id, value=button_no, user=username)
        session.add(reaction)
    else:
        for yr in your_reactions:
            session.delete(yr)
    session.commit()
    session.close()

    cb_buttons = [[InlineKeyboardButton("yes", callback_data="0"),
        InlineKeyboardButton("no", callback_data="1"),
        InlineKeyboardButton("err", callback_data="2"),
        InlineKeyboardButton("meToo", callback_data="3")]
    ]
    
    print("cb_buttonss == buttons")
    print(cb_buttons == buttons)
    #read reactions
    select = session.query(Reactions.value, func.count(Reactions.value)).filter(Reactions.message_id== query.inline_message_id).group_by(Reactions.value).all()
    
    if select:
        for tup in select:
            button_number = int(tup[0])
            button_count = str(tup[1])
            cb_buttons[0][button_number] = InlineKeyboardButton(buttonstext[button_number] + " + " + button_count, callback_data= str(button_number))
    print(buttons)

    client.edit_inline_reply_markup(
    query.inline_message_id,
    InlineKeyboardMarkup(cb_buttons))

app.run()



