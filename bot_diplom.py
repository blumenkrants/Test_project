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


# Ответ на любой текст
def talk_to_me(bot, update):
    user_text = update.message.text 
    update.message.reply_text('Нажмите /start чтобы записаться на услуги салона') 


# /start
def greet_user(bot, update):
  text = 'Вас приветствует salon_sevice_bot! Для записи нажмите "Записаться на услугу"'
  my_keyboard = ReplyKeyboardMarkup([['Записаться на услугу'],
                                   ['Мои записи', 'О нас']],
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
  update.message.reply_text(text, reply_markup=my_keyboard)


# Инлайн клавиатура с мастерами
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
    update.message.reply_text('Выберите мастера:', reply_markup=reply_markup)

# Обработчик контактов
def get_contact(bot, update, user_data):
    #print(update.message.contact)
    contact = update.effective_message.contact
    phone = contact.phone_number
    print(prhone)
    update.message.reply_text('Спасибо')

# Записываем контакты в базу
#def contacts2db(user_id,customer_name,customer_email,customer_phone_number):
#    print(user_id,customer_name,customer_email,customer_phone_number)
#    conn.execute('''CREATE TABLE IF NOT EXISTS userdetails(user_id int,customer_name text,customer_email text,customer_phone_number int )''')
#    conn.execute("INSERT INTO userdetails VALUES (?,?,?,?)",(user_id,customer_name,customer_email,customer_phone_number))
#    conn.commit()


# Инлайн клавиатуры
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

   
# Запрос контактов
    if len(query.data)==5:
        contact_button = KeyboardButton('Контактные данные', request_contact=True)
        my_keyboard = ReplyKeyboardMarkup([[contact_button]],
                                          resize_keyboard=True, 
                                          one_time_keyboard=True)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="Отправьте Ваши контактные данные для уточнения заказа:", 
                        reply_markup=my_keyboard)
        bot.delete_message(chat_id=update.callback_query.from_user.id,
                        message_id=query.message.message_id)
        
 #Альтернативный запрос контактов (телефон у пользователя не всегда правильный или вообше есть, ники тоже не всегда нормальные)
 #bot.send_message(chat_id=update.message.chat_id,text='Отправьте Ваши контактные данные для уточнения заказа в формате '
 #                                                        'Имя, Адрес почты, Телефон')
 #customer_name,customer_email,customer_phone_number=update.message.text.split(',')   
 #contacts2db(customer_name,customer_email,customer_phone_number)

# Запись всех данных в БД
        global p
        p = query.data
        user_data ['time'] = p
        # print(user_data)
        cort_1 = (user_data.get('name'), )
        cort_2 = cort_1 + (user_data.get('service'), )
        cort_3 = cort_2 + (user_data.get('date'), )
        cort_4 = cort_3 + (user_data.get('time'), )
        print(cort_4)
        data = []
        data.append(cort_4)
        cursor.executemany("INSERT INTO info VALUES (?,?,?,?)", data)
        conn.commit()


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
    bot.edit_message_text(chat_id=update.callback_query.from_user.id,
                        text="Выберите услугу: ", 
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)
    global d
    d = query.data


# Календарь    
    sql_3 = "SELECT service_name FROM table_services"
    cursor.execute(sql_3)
    data_base_3 = cursor.fetchall()
    for z in data_base_3:
        if query.data == z[0]:
                bot.edit_message_text(chat_id=update.callback_query.from_user.id,
                                    text="Выберите дату: ", 
                                    message_id=query.message.message_id,
                                    reply_markup=telegramcalendar.create_calendar())
                global e
                e = query.data


# Выбор времени
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        inline_keyboard = [[InlineKeyboardButton('10:00', callback_data ='10:00'),
                            InlineKeyboardButton('11:00', callback_data ='11:00')],
                            [InlineKeyboardButton('12:00', callback_data ='12:00'),
                            InlineKeyboardButton('13:00', callback_data ='13:00')],
                            [InlineKeyboardButton('14:00', callback_data ='14:00'),
                            InlineKeyboardButton('15:00', callback_data ='15:00')]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        bot.edit_message_text(chat_id=update.callback_query.from_user.id,
                            text="Вы выбрали дату: %s. Выберите удобное для Вас время: " % (date.strftime("%d/%m/%Y")),
                            message_id=query.message.message_id, 
                            reply_markup=reply_markup)


# Запись данных в user_data 
    user_data ['name'] = c
    user_data ['date'] = date.strftime("%d/%m/%Y")
    user_data ['service'] = e

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


# Кнопка о компании
def press_button4(bot, update, user_data):
    my_keyboard_2 = ReplyKeyboardMarkup([["Вернуться в меню"]], 
                                        resize_keyboard=True)
    bot.send_photo(chat_id=update.message.chat.id,
                   photo=open('/Users/dmitriy/Downloads/mapbrb.jpg', 'rb'))
    update.message.reply_text("Наши контакты: \n "
                              "Адрес: г.Москва, ул.Большая Ордынка 17 стр.1 \n"
                              " Телефон: +74951234567 \n"
                              " Часы работы: \n "
                              "Будни: с 10:00 до 22:00 \n"
                              " Выходные: c 12:00 до 22:00",
                              reply_markup=my_keyboard_2)


# Кнопка с информацией пользователя
def info(bot, update, user_data):
    my_keyboard_2 = ReplyKeyboardMarkup([["Вернуться в меню"]], 
                                        resize_keyboard=True)
    update.message.reply_text("Имя мастера: " + user_data.get('name') + "\n"
                                "Услуга: " + user_data.get('service') + "\n"
                                "Дата: " + user_data.get('date') + "\n"
                                "Время: " + user_data.get('time'))

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(CommandHandler("Вернуться в меню", greet_user))
    dp.add_handler(RegexHandler("Вернуться в меню", greet_user))

    dp.add_handler(CommandHandler('Записаться на услугу', inline_master, pass_user_data=True))
    dp.add_handler(RegexHandler('Записаться на услугу', inline_master, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(inline_master_pressed, pass_user_data=True))

    dp.add_handler(CommandHandler("О нас", press_button4, pass_user_data=True))
    dp.add_handler(RegexHandler("О нас", press_button4, pass_user_data=True))

    dp.add_handler(CommandHandler("Мои записи", info, pass_user_data=True))
    dp.add_handler(RegexHandler("Мои записи", info, pass_user_data=True))
             
    dp.add_handler(MessageHandler(Filters.contact, get_contact))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main ()
