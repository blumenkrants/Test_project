from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler

import telegramcalendar
import sqlite3

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

def talk_to_me(bot, update):
    user_text = update.message.text 
    update.message.reply_text('Приносим свои извинения! Бот находится в стадии разработки!')

def greet_user(bot, update):
  text = 'Приносим свои извинения! Бот находится в стадии разработки!'
  my_keyboard = ReplyKeyboardMarkup([['Записаться на услугу'],
                                   ['Мои записи', 'О нас']],
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
  update.message.reply_text(text, reply_markup=my_keyboard)

# инлайн клавиатура c именами
def inline_master(bot,update, user_data):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    sql = "SELECT barber_name FROM table_barbers"
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
    bot.send_photo(chat_id=update.message.chat.id,
                    photo=open('/Users/dmitriy/Downloads/barber.jpg', 'rb'))
    update.message.reply_text('Выберите мастера', reply_markup=reply_markup)

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Спасибо')

# Клавиатура с услугами
def inline_master_pressed(bot, update, user_data):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM table_barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_1 = "SELECT * FROM table_barbers2services"
    cursor.execute(sql_1)
    data_base_1 = cursor.fetchall()

    sql_2 = "SELECT * FROM table_services"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    counter = []
    query = update.callback_query
    name = query.data
    if len(query.data)==5:
        contact_button = KeyboardButton('Контактные данные', request_contact=True)
        my_keyboard = ReplyKeyboardMarkup([[contact_button]],
                                          resize_keyboard=True, 
                                          one_time_keyboard=True)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="Отправьте Ваши контактные данные для уточнения заказа:", 
                        reply_markup=my_keyboard)
        global p
        p = query.data
        print(p)

    # print(name)
    if name == query.data:
        global c
        c = query.data
        for masters in data_base:
            if name in masters:
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
                                keyboard.append(row)
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                bot.send_message(chat_id=update.callback_query.from_user.id,
                                            text="Выберите услугу: ", 
                                            reply_markup=reply_markup)
                                global d
                                d = query.data
    
    sql_3 = "SELECT service_name FROM table_services"
    cursor.execute(sql_3)
    data_base_3 = cursor.fetchall()
    for z in data_base_3:
        if query.data == z[0]:
                bot.send_message(chat_id=update.callback_query.from_user.id,
                                text="Выберите дату: ", 
                                reply_markup=telegramcalendar.create_calendar())
                global e
                e = query.data

    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        inline_keyboard = [[InlineKeyboardButton('10:00', callback_data ='10:00'),
                            InlineKeyboardButton('11:00', callback_data ='11:00')],
                            [InlineKeyboardButton('12:00', callback_data ='12:00'),
                            InlineKeyboardButton('13:00', callback_data ='13:00')],
                            [InlineKeyboardButton('14:00', callback_data ='14:00'),
                            InlineKeyboardButton('15:00', callback_data ='15:00')]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="Вы выбрали дату: %s. Выберите удобное для Вас время: " % (date.strftime("%d/%m/%Y")), 
                        reply_markup=reply_markup)

    # a = c + e + d
    # print(a)


    # my_keyboard_1 = ReplyKeyboardMarkup([counter,
    #                                     ["Вернуться в меню"]],
    #                                     resize_keyboard=True,
    #                                     one_time_keyboard=True)
    # bot.send_message(chat_id=update.callback_query.from_user.id,
    #                  text="Выберите услугу: ",
    #                  reply_markup=my_keyboard_1)

                        




    # date = update.callback_query
    # date_1 = query.data
    # print(date_1)
    # Удаление сообщений
    # bot.delete_message(message.chat.id, message.message_id)

        # a = date.strftime("%d/%m/%Y")

    # conn = sqlite3.connect('mydatabase.db')
    # cursor = conn.cursor()
    # clients = [(master1, a)]

    # cursor.executemany("INSERT INTO table_cal_types VALUES (?,?)", clients)
    # conn.commit()

# conn = sqlite3.connect('mydatabase.db')
# cursor = conn.cursor()
# sql = "SELECT * FROM table_cal_types"
# master1 = "SELECT * FROM table_cal_types WHERE cal_type_id='Мастер Мурад'"
# cursor.execute(master1)
# data_base = cursor.fetchone()
# data_base_1 = data_base[0]
# print(data_base)

# Календарь
# def calendar(bot, update):
#     bot.send_message(chat_id=update.callback_query.from_user.id,
#                     text="Please select a date: ",
#                      reply_markup=telegramcalendar.create_calendar())
#     selected,date = telegramcalendar.process_calendar_selection(bot, update)
#     if selected:
#         bot.send_message(chat_id=update.callback_query.from_user.id,
#                         text="You selected %s" % (date.strftime("%d/%m/%Y")), 
#                         reply_markup=ReplyKeyboardMarkup([['10:00', '11:00'],
#                                    ['12:00', '13:00']],
#                                    resize_keyboard=True))

# Кнопки
def calendar(bot, update):
    print('lol')
    # bot.send_message(chat_id=update.callback_query.from_user.id,
    #                 text="Вы выбрали дату: ", 
    #                 reply_markup=telegramcalendar.create_calendar())

def press_button4(bot, update):
    my_keyboard_2 = ReplyKeyboardMarkup([["Вернуться в меню"]], 
                                        resize_keyboard=True)
    update.message.reply_text("Здесь можно будет узнать о компании", 
                              reply_markup=my_keyboard_2)

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    # dp.add_handler(CommandHandler('Услуга: ', calendar))
    # dp.add_handler(RegexHandler('Услуга: ', calendar))

    dp.add_handler(CommandHandler("Вернуться в меню", greet_user))
    dp.add_handler(RegexHandler("Вернуться в меню", greet_user))

    dp.add_handler(CommandHandler('Записаться на услугу', inline_master, pass_user_data=True))
    dp.add_handler(RegexHandler('Записаться на услугу', inline_master, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(inline_master_pressed, pass_user_data=True))

    dp.add_handler(CommandHandler("О нас", press_button4))
    dp.add_handler(RegexHandler("О нас", press_button4))

    dp.add_handler(CommandHandler('Контактные данные', calendar))
    dp.add_handler(RegexHandler('Контактные данные', calendar))
             
    dp.add_handler(MessageHandler(Filters.contact, get_contact))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main ()