import gspread
import schedule
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('5305696037:AAHC7xzuBuGgR5gDUpZ_qJXUxpx-mKKah6E')

gc = gspread.service_account("token.json")

# Open a sheet from a spreadsheet in one go
wks_text = gc.open("test bot").worksheet("texts")
wks_authors = gc.open("test bot").worksheet("authors")
wks_academy = gc.open("test bot").worksheet("academy")


def get_stat():
    texts_lists = wks_text.get_all_values()
    text_todo_num = len(texts_lists)
    wks_anal = gc.open("test bot").worksheet("analytics")
    text_num = wks_anal.acell('A2').value
    if text_todo_num > int(text_num):
        wks_anal.update('A2', text_todo_num)
        send_new_text(text_todo_num)

    academy_list = wks_academy.get_all_values()
    academy_todo_num = len(academy_list)
    wks_anal = gc.open("test bot").worksheet("analytics")
    academy_num = wks_anal.acell('F2').value
    if academy_todo_num > int(academy_num):
        print(academy_num, 'academy_num')
        wks_anal.update('F2', academy_todo_num)
        print('updated', wks_anal.acell('F2').value)
        send_new_url(academy_todo_num)

    # if users haven sent any text
    # for i in []:
    #     if i == 0:
    #         for idx in [1:]
    #             send_new_url(idx)
    #             send_new_text(idx):


def send_new_url(row_id):
    ids = wks_authors.row_values(2)
    for id_author in ids:
        if len(id_author) > 1:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Send the link to Google doc", callback_data=f'link{row_id}'))
            bot.send_message(int(id_author), wks_academy.acell(f'A{row_id}').value, reply_markup=markup)

def send_new_text(row_id):
    ids = wks_authors.row_values(2)
    for id_author in ids:
        if len(id_author) > 1:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Send a translation", callback_data=f'text{row_id}'))
            bot.send_message(int(id_author), wks_text.acell(f'A{row_id}').value, reply_markup=markup)


def job():
    schedule.every(0.5).minutes.do(get_stat)
    while True:
        schedule.run_pending()
        time.sleep(1)


job()
