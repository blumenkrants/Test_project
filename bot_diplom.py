import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram import ReplyKeyboardRemove
import telegramcalendar
import sqlite3

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

TOKEN = "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo"


FIRST, SECOND, FIRD = range(3)

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

logger = logging.getLogger(__name__)

def calendar_handler(bot,update):
    # функция вызова инлайн клавиатур
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    sql = "SELECT * FROM barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_1 = "SELECT * FROM barbers_to_services"
    cursor.execute(sql_1)
    data_base_1 = cursor.fetchall()

    sql_2 = "SELECT * FROM services"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    query = update.callback_query
    name = query.data
# Клавиатура с услугами
    counter = []
    for masters in data_base:
        if name in masters:
            global c
            c = query.data
            a = masters[0]
            for master_id in data_base_1:
                if a in master_id:
                    b = master_id[2]
                    for service_id in data_base_2:
                        if b in service_id:
                            all_services = []
                            all_services.append(service_id[2])
                            keyboard = []
                            row = []
                            for i in all_services:
                                row.append(InlineKeyboardButton(i, callback_data=str(i)))
                            counter = row + counter
    list_1 = []
    list_1.append(counter)
    reply_markup = InlineKeyboardMarkup(list_1)

    bot.edit_message_text(text='Выберите услугу:',
                          chat_id=update.callback_query.from_user.id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return SECOND

def calendar_handler1(bot,update):
    query = update.callback_query

    bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=telegramcalendar.create_calendar())
    return FIRD

def time(bot,update):
    print('lol')
    query = update.callback_query
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=telegramcalendar.create_calendar())


def start(bot, update):
    # функция вызова инлайн клавиатуры с мастерами
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    sql = "SELECT barber_name FROM barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()
    all_masters = []
    for masters in data_base:
        all_masters.append(masters[0])
    keyboard = []
    row = []
    for i in all_masters:
        row.append(InlineKeyboardButton(i, callback_data=str(i)))
    keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # bot.send_photo(chat_id=update.message.chat.id,
    #                photo=open('C:\projects\diplom\photo\BRB 666.jpg', 'rb'))
    update.message.reply_text('Выберите мастера', reply_markup=reply_markup)
    return FIRST

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)
    dp = mybot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(calendar_handler)],
            SECOND: [CallbackQueryHandler(calendar_handler1)],
            FIRD: [CallbackQueryHandler(time)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
   main()