import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import gspread

bot = telebot.TeleBot('5305696037:AAHC7xzuBuGgR5gDUpZ_qJXUxpx-mKKah6E')
gc = gspread.service_account("token.json")

# Open a sheet from a spreadsheet in one go
wks_texts = gc.open("test bot").worksheet("texts")
wks_analytics = gc.open("test bot").worksheet("analytics")
wks_authors = gc.open("test bot").worksheet("authors")
wks_academy = gc.open("test bot").worksheet("academy")
lang_col = {"Turkish": 'B', "Spanish": 'C', "Portuguese": 'D', "Vietnamese": 'E'}

@bot.message_handler(commands=['start'])
def message_handler(message):
    mess = f'Hi! {message.from_user.first_name}, please choose the language you will translate into.'
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row_width = 4
    markup.add("Portuguese", "Spanish", "Vietnamese", "Turkish")
    msg = bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, save_author_data)


def save_author_data(message):
    col = f'{lang_col[message.text]}2'
    id_author = message.chat.id
    wks_authors.update(col, id_author)
    bot.send_message(message.chat.id, "Please wait the new texts (: We will send it to you here.")  # change phrase there

info = []

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    ids = wks_authors.row_values(2)
    print(ids)
    ids_dict = {ids[3]: 'D', ids[2]: 'C', ids[4]: 'E', ids[1]: 'B'}
    user_id = call.message.chat.id
    row = str(call.data[-1])
    col = ids_dict[str(user_id)]
    info.insert(0, col + row)
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Cancel")
    if call.data[:4] == 'text':
        msg = bot.send_message(user_id, 'Please send a translation of the text in reply message then it will be ready.', reply_markup=markup)
        bot.register_next_step_handler(msg, save_trans_text)
    elif call.data[:4] == 'link':
        msg = bot.send_message(user_id, 'Please send a link to Google doc with translation of the text in reply message then it will be ready.', reply_markup=markup)
        bot.register_next_step_handler(msg, save_trans_link)


def save_trans_text(message):
    if message.text != "Cancel":
        translation = message.text
        path = info[0]
        print(translation, path)
        wks_texts.update(path, translation)
        bot.send_message(message.chat.id, 'Thank you very much!')

def save_trans_link(message):
    if message.text != "Cancel":
        link = message.text
        path = info[0]
        print(link, path)
        wks_academy.update(path, link)
        bot.send_message(message.chat.id, 'Thank you very much!')


bot.polling(non_stop=True)
