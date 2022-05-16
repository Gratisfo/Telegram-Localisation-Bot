import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import gspread

bot = telebot.TeleBot('TOKEN')
gc = gspread.service_account("token.json")

# Open a sheet from a spreadsheet in one go
wks_texts = gc.open("test bot").worksheet("texts")
wks_analytics = gc.open("test bot").worksheet("analytics")
wks_authors = gc.open("test bot").worksheet("authors ")


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("Portuguese", callback_data="C2"),
               InlineKeyboardButton("Spanish", callback_data="B2"),
               InlineKeyboardButton("Vietnamese", callback_data="D2"),
               InlineKeyboardButton("Turkish", callback_data="A2"))
    return markup


def save_author_data(id, language):
    wks_authors.update(language, id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "C2":
        bot.answer_callback_query(call.id, "Answer is Portuguese")
        language = call.data
    elif call.data == "B2":
        bot.answer_callback_query(call.id, "Answer is Spanish")
        language = call.data
    elif call.data == "D2":
        bot.answer_callback_query(call.id, "Answer is Vietnamese")
        language = call.data
    elif call.data == "A2":
        bot.answer_callback_query(call.id, "Answer is Turkish")
        language = call.data
    bot.send_message(call.message.chat.id, f'We save you choice language, please wait the new text')
    save_author_data(call.message.chat.id, language)
    bot.send_message(call.message.chat.id, f'Please wait a new text for translation')


@bot.message_handler(commands=['start'])
def message_handler(message):
    mess = f'Hi! {message.from_user.first_name}, please choose the language you will translate into.'
    bot.send_message(message.chat.id, mess, reply_markup=gen_markup())


@bot.message_handler(func=lambda m: True)
def get_user_test(message):
    id = message.chat.id
    column = wks_authors.find(str(id)).col
    row = wks_analytics.acell('A2').value
    if column == 1:
        col = 'B'
    elif column == 2:
        col = 'C'
    elif column == 3:
        col = 'D'
    elif column == 4:
        col = 'E'

    wks_texts.update(col + str(row), message.text)


bot.infinity_polling()

bot.polling(non_stop=True)

