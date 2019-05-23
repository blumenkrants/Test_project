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
import datetime
from datetime import time, timedelta
from telegram.ext import messagequeue as mq





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
        update.message.reply_text(text, reply_markup=start_keyboard)
        global subscribers
        subscribers = update.message.chat_id
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
    sql = "SELECT service_name, price FROM services"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    all_price = []
    for price in data_base:
        all_price.append(price[1])

    all_masters = []
    for masters in data_base:
        all_masters.append(masters[0])
    keyboard = []
    row = []
    rows = []

    info_text = '{} - {} \n {} - {} \n {} - {} \n {} - {} \n'.format(all_masters[0], all_price[0],
                                                                    all_masters[1], all_price[1],
                                                                    all_masters[2], all_price[2],
                                                                    all_masters[3], all_price[3])

    for i in all_masters[0:2]:
        row.append(InlineKeyboardButton(i, callback_data=str(i)))
    for i in all_masters[2:4]:
        rows.append(InlineKeyboardButton(i, callback_data=str(i)))
            
    keyboard.append(row)
    keyboard.append(rows)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # bot.send_photo(chat_id=update.message.chat.id,
    #                 photo="http://nibler.ru/uploads/users/11119/2015-10-14/oblakah-fakty-interesnye-_189279796.jpg")
    #                # photo=open('C:\projects\diplom\photo\BRB 666.jpg', 'rb'))
    update.message.reply_text(info_text, reply_markup=reply_markup)
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

                            all_images = []
                            all_images.append(barber_name[2])
                            print(all_images)


                            # for i in all_barbers:
                            #     row.append(InlineKeyboardButton(i, callback_data=str(i)))
                            # counter = row + counter     
                            
                            for i in all_barbers:
                                row.append(InlineKeyboardButton(i, callback_data=str(i)))
                                list_1 = [row]
                                reply_markup = InlineKeyboardMarkup(list_1)
                                bot.send_photo(chat_id=update.callback_query.from_user.id,
                                                photo=all_images[0],
                                                caption='lol',
                                                reply_markup=reply_markup)
                                # bot.send_message(chat_id=update.callback_query.from_user.id,
                                #                      text='Мастер: ',
                                #                      reply_markup=reply_markup)
                                # можно вставить между этими функциями функцию, которая чистит диалог


    # list_1 = [counter]
    # reply_markup = InlineKeyboardMarkup(list_1)

    # bot.edit_message_text(text='Выберите мастера:',
    #                       chat_id=update.callback_query.from_user.id,
    #                       message_id=query.message.message_id,
    #                       reply_markup=reply_markup)

    # Запись данных в user_data
    user_data ['service'] = query.data
    return SECOND

def calendar(bot,update, user_data):
    # функция вызова календаря
    query = update.callback_query
    # bot.delete_message(chat_id=update.callback_query.from_user.id,
    #                     message_id=query.message.message_id)
    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text='Выберите дату: ',
                     reply_markup=telegramcalendar.create_calendar())

    # if query == "Вова":
    #     bot.edit_message_text(text='Выберите дату:',
    #                       chat_id=query.message.chat_id,
    #                       message_id=query.message.message_id,
    #                       reply_markup=telegramcalendar.create_calendar_vova())
    # else:
    #     bot.edit_message_text(text='Выберите дату: {}'.format(smile_5),
    #                           chat_id=query.message.chat_id,
    #                           message_id=query.message.message_id,
    #                           reply_markup=telegramcalendar.create_calendar())
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
        row_3 = [InlineKeyboardButton('Выбрать другой день', callback_data='Выбрать другой день')]

        for i in all_time[0:3]:
            row.append(InlineKeyboardButton(i, callback_data=str(i)))
        for i in all_time[3:6]:
            row_2.append(InlineKeyboardButton(i, callback_data=str(i)))

        keyboard.append(row)
        keyboard.append(row_2)
        keyboard.append(row_3)

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
    elif query.data == "Выбрать другой день":
        bot.edit_message_text(text = 'lolkin',
                                chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=telegramcalendar.create_calendar_vova())
        return THIRD
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
    user_data['number'] = update.message.contact.phone_number
    user_data['first_name'] = update.message.contact.first_name
    user_data['last_name'] = update.message.contact.last_name

    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню {}'.format(smile_13)],
                                      ['Отправить напоминание']],
                                      resize_keyboard=True)

    update.message.reply_text("Спасибо! \n "
                              "Вы можете посмотреть информацию о своих записях в главном меню",
                              reply_markup=my_keyboard)

    """Запись всех данных в БД"""
    record = (user_data.get('service'),
              user_data.get('name'),
              user_data.get('date'),
              user_data.get('time'),
              user_data.get('number'),
              user_data.get('first_name'),
              user_data.get('last_name'),
              )

    record_insert = "INSERT INTO record_info (service, name, date, time, number, first_name, last_name)" \
                    " VALUES (%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(record_insert, record)
    conn.commit()
    # cursor.close()
    # conn.close()

#создание времени для уведомления о записи
    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    zapis_1 = []

    for z in data_base:
        if user_data.get('number') == z[4]:
            zapis_1.extend((z[2:4]))

    top_zapis = (' '.join(zapis_1[0:2]))
    dates = datetime.datetime.strptime(top_zapis, "%Y-%m-%d %H:%M")
    lolkin = timedelta(hours=6, minutes=13)
    global topcheg
    topcheg = dates + lolkin
    print(topcheg)

    top_zapis_2 = (' '.join(zapis_1[2:4]))
    dates_2 = datetime.datetime.strptime(top_zapis_2, "%Y-%m-%d %H:%M")
    lolkin_2 = timedelta(hours=6, minutes=14)
    global topcheg_2
    topcheg_2 = dates_2 + lolkin_2
    print(topcheg_2)

    top_zapis_3 = (' '.join(zapis_1[4:6]))
    dates_3 = datetime.datetime.strptime(top_zapis_3, "%Y-%m-%d %H:%M")
    lolkin_3 = timedelta(hours=6, minutes=15)
    global topcheg_3
    topcheg_3 = dates_3 + lolkin_3
    print(topcheg_3)
    

def my_entry(bot, update, user_data):
    # функция вывод информации о записях
    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_2 = "SELECT * FROM services"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    if user_data == {}:
        update.message.reply_text('У вас нет записей {}'.format(smile_10),
                                  reply_markup=start_keyboard)
    else:
        check_price = []

        row = []
        row_1 = []
        row_2 = []
        all_entries = []
        main_menu = []

        info = []

        keyboard = []

        for z in data_base:
            if user_data.get('number') == z[4]:
                info.extend((z[0:4]))
                for m in data_base_2:
                    if z[0] in m[2]:
                        check_price.append(m[3])
        total_sum = sum(check_price[0:])

        if len(info) == 4:
            row.append(InlineKeyboardButton((', '.join(info[0:4])), callback_data='1'))
            main_menu.append(InlineKeyboardButton('Вернуться в главное меню {}'.format(smile_13), callback_data='0'))
            keyboard.extend((row, main_menu))
        elif len(info) == 8:
            row.append(InlineKeyboardButton((', '.join(info[0:4])), callback_data='1'))
            row_1.append(InlineKeyboardButton((', '.join(info[4:8])), callback_data='2'))
            all_entries.append(InlineKeyboardButton('Отменить все записи {}'.format(smile_4), callback_data='Отмена'))
            main_menu.append(InlineKeyboardButton('Вернуться в главное меню {}'.format(smile_13), callback_data='0'))
            keyboard.extend((row, row_1, all_entries, main_menu))
        elif len(info) > 8:
            row.append(InlineKeyboardButton((', '.join(info[0:4])), callback_data='1'))
            row_1.append(InlineKeyboardButton((', '.join(info[4:8])), callback_data='2'))
            row_2.append(InlineKeyboardButton((', '.join(info[8:12])), callback_data='3'))
            all_entries.append(InlineKeyboardButton('Отменить все записи {}'.format(smile_4), callback_data='Отмена'))
            main_menu.append(InlineKeyboardButton('Вернуться в главное меню {}'.format(smile_13), callback_data='0'))
            keyboard.extend((row, row_1, row_2, all_entries, main_menu))

        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            update.message.reply_text('Клиент: ' + user_data.get('first_name') + '\n'
                                      + '\n'
                                      'Итоговая сумма: ' + str(total_sum) + '\n'
                                      + '\n'
                                      'Ниже представлена краткая информация о ваших записях.' + '\n'
                                      'Чтобы отменить запись -  просто нажмите на нее!',
                                      reply_markup=reply_markup)
        except AttributeError:
            bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=reply_markup)

        return FIVE


def cancel_entries(bot, update, user_data, job_queue):
    # информация о записях, а также их отмена по одной
    query = update.callback_query
    service = query.data

    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    info_list = []
    for data_list in data_base:
        if user_data.get('number') in data_list[4]:
            info_list.extend((data_list[0:4]))

    if service == '1' and len(info_list) == 4:
        a = (info_list[0], info_list[1], info_list[2], info_list[3], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and name = %s and date = %s and time = %s and number = %s", a)
        user_data.clear()
        conn.commit()
        #Отменяет уведомление
        job_queue.stop()

        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='У вас нет записей {}'.format(smile_10),
                         reply_markup=start_keyboard)
    elif service == '1':
        a = (info_list[0], info_list[1], info_list[2], info_list[3], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and name = %s and date = %s and time = %s and number = %s", a)
        conn.commit()
        #Отменяет уведомление
        if len(info_list) == 12:
            counter[0].schedule_removal()
        if len(info_list) == 8:
            counter[1].schedule_removal()
        
    elif service == '2':
        a = (info_list[4], info_list[5], info_list[6], info_list[7], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and name = %s and date = %s and time = %s and number = %s", a)
        conn.commit()
        # #Отменяет уведомление
        if len(info_list) == 12:
            counter[1].schedule_removal()
        if len(info_list) == 8:
            counter[2].schedule_removal()

    elif service == '3':
        a = (info_list[8], info_list[9], info_list[10], info_list[11], user_data.get('number'))
        cursor.execute("DELETE FROM record_info WHERE service = %s and name = %s and date = %s and time = %s and number = %s", a)
        conn.commit()
        #Отменяет уведомление
        counter[2].schedule_removal()
    elif service == 'Отмена':
        a = user_data.get('number')
        cursor.execute("DELETE FROM record_info WHERE number = %s" % a)
        user_data.clear()
        conn.commit()
        #Отменяет уведомление
        job_queue.stop()

        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='У вас нет записей {}'.format(smile_10),
                         reply_markup=start_keyboard)
    elif service == '0':
        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='Вы вернулись в главное меню',
                         reply_markup=start_keyboard)

    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text='Есть!',
                     reply_markup=my_entry(bot, update, user_data))


def set_alarm(bot, update, job_queue, user_data):
    query = update.callback_query

    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    vse_zapisi = []
    
    global info_9
    info_9 = []

    for z in data_base:
        if user_data.get('number') == z[4]:
            vse_zapisi.append(z[4])
            info_9.extend((z[0:4]))

    if len(vse_zapisi) == 1:
        job_queue.run_once(alarm, when=topcheg, context=update.message.chat_id, name='lol')
    elif len(vse_zapisi) == 2:
        job_queue.run_once(alarm_1, when=topcheg_2, context=update.message.chat_id, name='lol')
    elif len(vse_zapisi) == 3:
        job_queue.run_once(alarm_2, when=topcheg_3, context=update.message.chat_id, name='lol')

    global counter
    counter = []
# добавляет все созданные напоминания в список
    for job in job_queue.get_jobs_by_name('lol'):
        counter.append(job)

    update.message.reply_text("Напоминание создано!",
                              reply_markup=start_keyboard)


@mq.queuedmessage
def alarm(bot, job):
    bot.send_message(chat_id=job.context, text=('Запись 1 ' + ', '.join(info_9[0:4])))
    # 'Напоминаем, что Вы записаны на услугу {} к мастеру {} через 1 час!'.format(info_9[0], info_9[1])

@mq.queuedmessage
def alarm_1(bot, job):
    bot.send_message(chat_id=job.context, text=('Запись 2 ' + ', '.join(info_9[4:8])))

@mq.queuedmessage
def alarm_2(bot, job):
    bot.send_message(chat_id=job.context, text=('Запись 3 ' + ', '.join(info_9[8:12])))




def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default = True

    conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Запись', choose_master, pass_user_data=True),
                      RegexHandler('Добавить Запись', choose_master, pass_user_data=True),
                      RegexHandler('Вернуться к началу', choose_master, pass_user_data=True),
                      RegexHandler('Мои записи', my_entry, pass_user_data=True)],
        states={FIRST: [CallbackQueryHandler(choose_service, pass_user_data=True)],
                SECOND: [CallbackQueryHandler(calendar, pass_user_data=True)],
                THIRD: [CallbackQueryHandler(time, pass_user_data=True)],
                FOURTH: [CallbackQueryHandler(contact, pass_user_data=True)],
                FIVE: [CallbackQueryHandler(cancel_entries, pass_user_data=True, pass_job_queue=True)]},
        fallbacks=[MessageHandler(Filters.contact, get_contact, pass_user_data=True)],
        allow_reentry=True)

    dp.add_handler(conv_handler)
    
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler('Запись', choose_master, pass_user_data=True))
    dp.add_handler(RegexHandler('Запись', choose_master, pass_user_data=True))

    dp.add_handler(CommandHandler("Отправить напоминание", set_alarm, pass_job_queue=True, pass_user_data=True))
    dp.add_handler(RegexHandler("Отправить напоминание", set_alarm, pass_job_queue=True, pass_user_data=True))


    # dp.add_handler(CommandHandler("О нас", callback_timer))
    # dp.add_handler(RegexHandler("О нас", callback_timer))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
   main()