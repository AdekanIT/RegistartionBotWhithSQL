import telebot
from geopy import Nominatim
from telebot.types import ReplyKeyboardRemove
import database as db
import buttons as bt
import sqlite3
import types

bot = telebot.TeleBot('6711309319:AAEgBRjAlC8HkAuf0z_XQIQ1SOoT2UZFjqc')
geolocation = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                   '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check = db.checker(user_id)
    bot.send_message(user_id, 'Please choice language!', reply_markup=bt.lang())
    bot.register_next_step_handler(message, language_choice)

def language_choice(message):
    user_id = message.from_user.id
    check = db.checker(user_id)

    # Checking the selected language
    if message.text.lower() == 'en':
        if check:
            bot.send_message(user_id, f'Hello {message.from_user.first_name}!\n'
                                      'Welcome back!')
        else:
            bot.send_message(user_id, f'Hello {message.from_user.first_name}!\n'
                                      "Welcome to the registration bot. "
                                      "Let's register you!\n"
                                      "Please enter your name")
            bot.register_next_step_handler(message, regist_en)
    elif message.text.lower() == 'ru':
        if check:
            bot.send_message(user_id, f'Привет {message.from_user.first_name}!\n'
                                      'С возвращением!')
        else:
            bot.send_message(user_id, f'Привет {message.from_user.first_name}!\n'
                                      "Добро пожаловать на регистрацию бота. "
                                      "Давайте вас зарегистрируем!\n"
                                      "Пожалуйста, введите ваше имя")
            bot.register_next_step_handler(message, regist_ru)


@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Commands\n'
                     '/help to show all commands\n'
                     '/help_me to contact us\n'
                     '/info for see your information\n'
                     '/register to registration')


@bot.message_handler(commands=['help_me'])
def help_me(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Admin: @AADEMAN\n'
                     'Phon number: +9989100XXXXX\n'
                     'E-mail: dxxxxxxxxx@gmail.com')


def regist_en(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Name added! Now, please share your phone number:', reply_markup=bt.num_bt())
    bot.register_next_step_handler(message, regist_phone_num_en, name)


def regist_ru(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Имя добавлено! А теперь поделитесь, пожалуйста, своим номером телефона:',
                     reply_markup=bt.num_bt())
    bot.register_next_step_handler(message, regist_phone_num_ru, name)


def regist_phone_num_en(message, name):
    user_id = message.from_user.id
    if message.contact:
        num = message.contact.phone_number
        bot.send_message(user_id, 'Incredible! Last step, please send your location',
                         reply_markup=bt.loc_bt())
        # Link for take location
        bot.register_next_step_handler(message, regist_location_en, name, num)
    else:
        # If user didn't send number by button
        bot.send_message(user_id, 'Please send your phone number by button!',
                         reply_markup=bt.num_bt())
        bot.register_next_step_handler(message, regist_phone_num_en, name)


def regist_phone_num_ru(message, name):
    user_id = message.from_user.id
    if message.contact:
        num = message.contact.phone_number
        bot.send_message(user_id, 'Невероятный! Последний шаг. Отправьте свое местоположение.',
                         reply_markup=bt.loc_bt())
        # Link for take location
        bot.register_next_step_handler(message, regist_location_ru, name, num)
    else:
        # If user didn't send number by button
        bot.send_message(user_id, 'Пожалуйста, отправьте свой номер телефона по кнопке!',
                         reply_markup=bt.num_bt())
        bot.register_next_step_handler(message, regist_phone_num_ru, name)


def regist_location_en(message, name, num):
    user_id = message.from_user.id
    if message.location:
        location = str(geolocation.reverse(f'{message.location.latitude},'
                                           f'{message.location.longitude}'))
        db.register(user_id, name, num, location)

        bot.send_message(user_id, 'Amazing! Registration done!',
                         reply_markup=ReplyKeyboardRemove())
    else:
        # If user didn't send location by button
        bot.send_message(user_id, 'Please send your location by button!',
                         reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, regist_location_en, name, num)


def regist_location_ru(message, name, num):
    user_id = message.from_user.id
    if message.location:
        location = str(geolocation.reverse(f'{message.location.latitude},'
                                           f'{message.location.longitude}'))
        db.register(user_id, name, num, location)

        bot.send_message(user_id, 'Удивительный! Регистрация завершена!',
                         reply_markup=ReplyKeyboardRemove())
    else:
        # If user didn't send location by button
        bot.send_message(user_id, 'Пожалуйста, отправьте свое местоположение с помощью кнопки!',
                         reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, regist_location_ru, name, num)


@bot.message_handler(commands=['info'])
def info_user(message):
    user_id = message.from_user.id
    user_info = db.show_info(user_id)
    if user_info:
        bot.send_message(user_id, f'User Information:\nName: {user_info[0]}\nPhone: {user_info[1]}\nLocation: {user_info[2]}')
    else:
        bot.send_message(user_id, 'User information not found.')


bot.polling(non_stop=True)









