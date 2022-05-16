import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import gspread

bot = telebot.TeleBot('5305696037:AAHC7xzuBuGgR5gDUpZ_qJXUxpx-mKKah6E')
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

# @bot.message_handler(commands=['start'])
# def start(message):
#     mess = f'Hi! {message.from_user.first_name}, please choose the language you will translate into.'
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 4
#     markup.add(types.InlineKeyboardButton("Portuguese", callback_data = "por"),
#                 types.InlineKeyboardButton("Spanish", callback_data = "esp"),
#                 types.InlineKeyboardButton("Vietnamese", callback_data = "vie"),
#                 types.InlineKeyboardButton("Turkish", callback_data = "tur"))
#
#     bot.send_message(message.chat.id, mess, reply_markup=markup)
#

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, message)

# @bot.message_handler()
# def get_user_test(message):
#     if message.text =="Hello!":
#         bot.send_message(message.chat.id, 'Hi there!')
#     elif message.text == "id":
#         bot.send_message(message.chat.id, f'your id is {message.from_user.id}')
#     else:
#         bot.send_message(message.chat.id, 'I do not understand you')
#
# @bot.message_handler(commands=['test'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Visit Site", url='https://github.com'))
#     bot.send_message(message.chat.id, 'Go to site', reply_markup=markup)
#
#
#
# @bot.message_handler(commands=['help'])
# def website(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     website = types.KeyboardButton('Website')
#     start = types.KeyboardButton("Start")
#     markup.add(website, start)
#     bot.send_message(message.chat.id, 'Go to site', reply_markup=markup)


# list_of_lists = wks_texts.get_all_values()
# for_translation = len(list_of_lists)
#
# text_num = wks_analytics.acell('A2').value
# print(text_num)
# if for_translation > int(text_num):
#     wks_analytics.update('A2', for_translation)
