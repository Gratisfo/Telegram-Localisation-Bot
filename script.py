import gspread
import schedule
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot('TOKEN')


gc = gspread.service_account("token.json")

# Open a sheet from a spreadsheet in one go
wks_text = gc.open("test bot").worksheet("texts")
wks_authors = gc.open("test bot").worksheet("authors ")
try:
    id_esp = int(wks_authors.acell('B2').value)
except:
    id_esp = False

try:
    id_tur = int(wks_authors.acell('A2').value)
except:
    id_tur = False
try:
    id_por = int(wks_authors.acell('C2').value)
except:
    id_por = False
try:
    id_vn = int(wks_authors.acell('D2').value)
except:
    id_vn = False




# # Format the header
def get_stat():
    list_of_lists = wks_text.get_all_values()
    for_trans = len(list_of_lists)
    print(for_trans)
    wks_anal = gc.open("test bot").worksheet("analytics")
    text_num = wks_anal.acell('A2').value
    if for_trans > int(text_num):
        wks_anal.update('A2', for_trans)
        if id_esp:
            bot.send_message(id_esp, wks_text.acell(f'A{for_trans}').value)
        if id_tur:
            bot.send_message(id_tur, wks_text.acell(f'A{for_trans}').value)
        if id_por:
            bot.send_message(id_por, wks_text.acell(f'A{for_trans}').value)
        if id_vn:
            bot.send_message(id_vn, wks_text.acell(f'A{for_trans}').value)




def job():
    schedule.every(0.5).minutes.do(get_stat)
    while True:
        schedule.run_pending()
        time.sleep(1)

job()






