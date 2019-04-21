from __future__ import print_function
import datetime
import pickle
import os.path
from emoji import emojize
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, RegexHandler
import logging
import mysql.connector
import telegramcalendar


PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

TOKEN = "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo"

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD, FOURTH, FIVE = range(5)

conn = mysql.connector.connect(host='mysql.j949396.myjino.ru', 
                               database='j949396', 
                               user='j949396', 
                               password='qwerty')
cursor = conn.cursor()

# Список эмодзи
# smile = emojize(':memo:', use_aliases=True)
# smile_2 = emojize(':clock8:', use_aliases=True)
# smile_3 = emojize(':convenience_store:', use_aliases=True)
# smile_4 = emojize(':no_entry_sign:', use_aliases=True)
# smile_5 = emojize(':heavy_plus_sign:', use_aliases=True)
# smile_6 = emojize(':back:', use_aliases=True)

smile = emojize(':heavy_plus_sign:', use_aliases=True)
smile_2 = emojize(':ledger:', use_aliases=True)
smile_3 = emojize(':information_source:', use_aliases=True)
smile_4 = emojize(':x:', use_aliases=True)
smile_5 = emojize(':calendar:', use_aliases=True)
smile_6 = emojize(':man:', use_aliases=True)
smile_7 = emojize(':scissors:', use_aliases=True)
smile_8 = emojize(':clock230:', use_aliases=True)
smile_9 = emojize(':white_check_mark:', use_aliases=True)
smile_10 = emojize(':no_entry_sign:', use_aliases=True)
smile_11 = emojize(':iphone:', use_aliases=True)
smile_12 = emojize(':barber:', use_aliases=True)
smile_13 = emojize(':leftwards_arrow_with_hook:', use_aliases=True)



start_keyboard = ReplyKeyboardMarkup([['Запись {}'.format(smile)],
                                   ['Мои записи {}'.format(smile_2), 
                                    'О нас {}'.format(smile_3)]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
def talk_to_me(bot, update):
    # функция - ответ на текст введенный пользователем
    update.message.reply_text('Нажмите /start для запуска бота')

def greet_user(bot, update, user_data):
    # функция - /start
    if user_data == {}:
        text = 'Вас приветствует salon_service_bot!'
        # my_keyboard = ReplyKeyboardMarkup([['Запись {}'.format(smile)],
        #                                    ['Мои записи {}'.format(smile_2), 
        #                                     'О нас {}'.format(smile_3)]],
        #                                   resize_keyboard=True,
        #                                   one_time_keyboard=True)
        update.message.reply_text(text, reply_markup=start_keyboard)
    else: 
        text_2 = 'Выберите дальнейшее действие'
        my_keyboard_2 = ReplyKeyboardMarkup([['Мои записи{}'.format(smile_2)],
                                            ['Отменить все записи{}'.format(smile_4), 
                                             'Добавить Запись{}'.format(smile_5)]],
                                  resize_keyboard=True,
                                  one_time_keyboard=True)
        update.message.reply_text(text_2, reply_markup=my_keyboard_2)

def choose_master(bot, update, user_data):
    # функция вызова инлайн клавиатуры с мастерами 
    sql = "SELECT service_name FROM services"
    cursor.execute(sql)
    data_base = cursor.fetchall()
    all_masters = []
    for masters in data_base:
        all_masters.append(masters[0])
    keyboard = []
    row = []
    rows = []
    for i in all_masters[0:2]:
        row.append(InlineKeyboardButton(i, callback_data=str(i)))
    for i in all_masters[2:4]:
        rows.append(InlineKeyboardButton(i, callback_data=str(i)))
            
    keyboard.append(row)
    keyboard.append(rows)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # bot.send_photo(chat_id=update.message.chat.id,
    #                photo=open('C:\projects\diplom\photo\BRB 666.jpg', 'rb'))
    update.message.reply_text('Выберите услугу', reply_markup=reply_markup)
    return FIRST

def choose_service(bot,update, user_data):
    # функция вызова инлайн клавиатуры с услугами
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
    for service_id in data_base_2:
        if name in service_id:
            a = service_id[0] 
            for barber_id in data_base_1:
                if a in barber_id:
                    b = barber_id[1]
                    for barber_name in data_base:
                        if b in barber_name:
                            all_barbers = []
                            all_barbers.append(barber_name[1])
                            keyboard = []
                            row = []
                            for i in all_barbers:
                                row.append(InlineKeyboardButton(i, callback_data=str(i)))
                            counter = row + counter
    list_1 = []
    list_1.append(counter)
    reply_markup = InlineKeyboardMarkup(list_1)

    bot.edit_message_text(text='Выберите мастера:',
                          chat_id=update.callback_query.from_user.id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    # Запись данных в user_data
    user_data ['service'] = query.data
    return SECOND

def calendar(bot,update, user_data):
    # функция вызова календаря
    query = update.callback_query
    bot.edit_message_text(text='Выберите дату:',
                          chat_id=update.callback_query.from_user.id,
                          message_id=query.message.message_id,
                          reply_markup=telegramcalendar.create_calendar_vova())
    user_data ['name'] = query.data
    return THIRD


def time(bot,update, user_data):
    # функция вызова инлайн клавиатуры с временем
    query = update.callback_query
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    
    sql = "SELECT * FROM time_to_barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_2 = "SELECT * FROM record_info"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    # проверка по записанным клиентам
    if selected:
        all_time = []
        for name_list in data_base:
            if user_data.get('name') in name_list[0]:
                all_time.append(name_list[1])
        for time_info in data_base_2:
            if user_data.get('name') in time_info[1]:
                if date.strftime("%Y-%m-%d") in time_info[2]:
                    if time_info[3] in all_time:
                        all_time.remove(time_info[3])
                        if len(all_time) < 6:
                            all_time.append('Нет записи')

        keyboard = []
        row = []
        row_2 = []
        for i in all_time[0:3]:
            row.append(InlineKeyboardButton(i, callback_data=str(i)))
        for i in all_time[3:6]:
            row_2.append(InlineKeyboardButton(i, callback_data=str(i)))

        keyboard.append(row)
        keyboard.append(row_2)
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text='Выберите время:',
                              chat_id=update.callback_query.from_user.id,
                              message_id=query.message.message_id)
        bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=reply_markup)
    user_data ['date'] = date.strftime("%Y-%m-%d")
    return FOURTH

def contact (bot,update, user_data):
    # функция вызова запроса контактов
    query = update.callback_query
    if query.data == "Нет записи":
        bot.answer_callback_query(callback_query_id= query.id)
    else:
        contact_button = KeyboardButton('Контактные данные', request_contact=True)
        my_keyboard = ReplyKeyboardMarkup([[contact_button]],
                                          resize_keyboard=True,
                                          one_time_keyboard=True)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text="Отправьте Ваши контактные данные для уточнения заказа:",
                         reply_markup=my_keyboard)
        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        user_data ['time'] = query.data

def get_contact(bot, update, user_data):
    # функция обработчик контактов
    user_data ['number'] = update.message.contact.phone_number
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню {}'.format(smile_6)]],
                                      resize_keyboard=True)
    update.message.reply_text("Спасибо! \n"
                              "Вы можете посмотреть информацию о своих записях в главном меню",
                              reply_markup=my_keyboard)
    print(user_data)


    #создание события в гугл календаре
    # creds = None
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # service = build('calendar', 'v3', credentials=creds)
    # event = {
    #         'summary': '%s' % user_data.get('service'),
    #         'description': 'Мастер: %s, Номер клиента: %s' % (user_data.get('name'), user_data.get('phone')),
    #         'start':  {'dateTime': '%sT%s:00+03:00' % (user_data.get('date'), user_data.get('time'))},
    #         'end':    {'dateTime': '%sT%s:00+02:00' % (user_data.get('date'), user_data.get('time'))},
    #         }
    # event = service.events().insert(calendarId='primary', body=event).execute()
    # print ('Event created: %s' % (event.get('htmlLink')))


    # Запись всех данных в БД
    cort_1 = (user_data.get('name'),)
    cort_2 = cort_1 + (user_data.get('service'),)
    cort_3 = cort_2 + (user_data.get('date'),)
    cort_4 = cort_3 + (user_data.get('time'),)
    cort_5 = cort_4 + (user_data.get('number'),)
    data = []
    data.append(cort_5)
    cursor.execute("INSERT INTO record_info (name, service, date, time, number) VALUES (%s, %s, %s, %s, %s)", cort_5)
    conn.commit()
    # cursor.close()
    # conn.close()
    
def my_entry(bot, update, user_data):
    # функция вывод информации о записях


    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    # print(data_base)
    row = []
    row_1 = []
    row_2 = []
    all_entries = []
    menu = []

    x = []

    keyboard = []

    for z in data_base:
        if user_data.get('number') == z[4]:
            x.extend((z[0], z[1], z[3]))
    # print(x)

    if len(x) == 3:
        row.append(InlineKeyboardButton((x[0] + ', ' + x[1] + ', ' + x[2]), callback_data=1))
        keyboard.append(row)
    elif len(x) == 6:
        row.append(InlineKeyboardButton((x[0] + ', ' + x[1] + ', ' + x[2]), callback_data=1))
        row_1.append(InlineKeyboardButton((x[3] + ', ' + x[4] + ', ' + x[5]), callback_data=2))
        all_entries.append(InlineKeyboardButton('!!! Отменить все записи !!!', callback_data='Отменить все записи'))
        keyboard.extend((row, row_1, all_entries))
    elif len(x) > 6:
        row.append(InlineKeyboardButton((x[0] + ', ' + x[1] + ', ' + x[2]), callback_data=1))
        row_1.append(InlineKeyboardButton((x[3] + ', ' + x[4] + ', ' + x[5]), callback_data=2))
        row_2.append(InlineKeyboardButton((x[6] + ', ' + x[7] + ', ' + x[8]), callback_data=3))
        all_entries.append(InlineKeyboardButton('!!! Отменить все записи !!!', callback_data='Отменить все записи'))
        keyboard.extend((row, row_1, row_2, all_entries))


    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Клиент:',
                              reply_markup=reply_markup)


    return FIVE


def cancel_entries(bot, update, user_data):
    # информация о записях, а также их отмена по одной
    query = update.callback_query
    service = query.data

    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    #удалить потом
    sql_2 = "SELECT number FROM record_info"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    info_list = []
    for data_list in data_base:
        if user_data.get('number') in data_list[4]:
            info_list.append(data_list[0])

    if service == '1':
        a = (info_list[0], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and number = %s", a)
        conn.commit()
        print('Запись отменена!')

    elif service == '2':
        a = (info_list[1], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and number = %s", a)
        conn.commit()
        print('Запись отменена!')
        # update.message.reply_text('Запись отменена!', reply_markup=my_entry(bot, update, user_data))

    elif service == '3':
        a = (info_list[2], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and number = %s", a)
        conn.commit()
        print('Запись отменена!')
        # update.message.reply_text('Запись отменена!', reply_markup=my_entry(bot, update, user_data))

    elif service == 'Отменить все записи':
        # переделать блок
        for record in data_base_2:
            a = user_data.get('number')
            cursor.execute("DELETE FROM record_info WHERE number = %s" % a)
            print('Отменены все записи!')
            conn.commit()

    del_process(bot, update, user_data)

def del_process(bot, update, user_data):
    query = update.callback_query
    print(query.data)

    if query.data == 'Отменить все записи':
        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='У вас нет записей {}'.format(smile_10),
                         reply_markup=start_keyboard)

    else:
        sql = "SELECT * FROM record_info"
        cursor.execute(sql)
        data_base = cursor.fetchall()

        # print(data_base)
        row = []
        row_1 = []
        row_2 = []
        all_entries = []
        menu = []

        x = []

        keyboard = []

        for z in data_base:
            if user_data.get('number') == z[4]:
                x.extend((z[0], z[1], z[3]))
        print(x)


        if len(x) == 3:
            row.append(InlineKeyboardButton((x[0] + ', ' + x[1] + ', ' + x[2]), callback_data=1))
            keyboard.append(row)
        elif len(x) == 6:
            row.append(InlineKeyboardButton((x[0] + ', ' + x[1] + ', ' + x[2]), callback_data=1))
            row_1.append(InlineKeyboardButton((x[3] + ', ' + x[4] + ', ' + x[5]), callback_data=2))
            all_entries.append(InlineKeyboardButton('!!! Отменить все записи !!!', callback_data='Отменить все записи'))
            keyboard.extend((row, row_1, all_entries))
        elif len(x) > 6:
            row.append(InlineKeyboardButton((x[0] + ', ' + x[1] + ', ' + x[2]), callback_data=1))
            row_1.append(InlineKeyboardButton((x[3] + ', ' + x[4] + ', ' + x[5]), callback_data=2))
            row_2.append(InlineKeyboardButton((x[6] + ', ' + x[7] + ', ' + x[8]), callback_data=3))
            all_entries.append(InlineKeyboardButton('!!! Отменить все записи !!!', callback_data='Отменить все записи'))
            keyboard.extend((row, row_1, row_2, all_entries))
        else:
            bot.send_message(chat_id=update.callback_query.from_user.id,
                            text='У вас нет записей {}'.format(smile_10),
                            reply_markup=start_keyboard)


        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=reply_markup)


def delete_all(bot, update, user_data):
    sql = "SELECT number FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()
    for phone in data_base:
        a = user_data.get('number')
        cursor.execute("DELETE FROM record_info WHERE number =  %s" % a)
        conn.commit()
    user_data.clear()
    greet_user(bot, update, user_data)

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)
    
    dp = mybot.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Запись', choose_master, pass_user_data=True),
                      RegexHandler('Добавить Запись', choose_master, pass_user_data=True),
                      RegexHandler('Вернуться к началу', choose_master, pass_user_data=True),
                      RegexHandler('Мои записи', my_entry, pass_user_data=True)],
        states={FIRST: [CallbackQueryHandler(choose_service, pass_user_data=True)],
                SECOND: [CallbackQueryHandler(calendar, pass_user_data=True)],
                THIRD: [CallbackQueryHandler(time, pass_user_data=True)],
                FOURTH: [CallbackQueryHandler(contact, pass_user_data=True)],
                FIVE: [CallbackQueryHandler(cancel_entries, pass_user_data=True)]},
        fallbacks=[MessageHandler(Filters.contact, get_contact, pass_user_data=True)],
        allow_reentry=True)

    dp.add_handler(conv_handler)
    
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    
    # dp.add_handler(CommandHandler("Мои записи", my_entry, pass_user_data=True))
    # dp.add_handler(RegexHandler("Мои записи", my_entry, pass_user_data=True))

    dp.add_handler(CommandHandler("Отменить все записи", delete_all, pass_user_data=True))
    dp.add_handler(RegexHandler("Отменить все записи", delete_all, pass_user_data=True))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler('Запись', choose_master, pass_user_data=True))
    dp.add_handler(RegexHandler('Запись', choose_master, pass_user_data=True))

    # dp.add_handler(CommandHandler("О нас", info))
    # dp.add_handler(RegexHandler("О нас", info))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
   main()