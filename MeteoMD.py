import urllib.request
from bs4 import BeautifulSoup as bs
import re
import telebot
from datetime import datetime

token = '530241878:AAE5Up637Bs0INqgsQM4HFcur2zeIW5ysoQ'
TelegramBot = telebot.TeleBot(token)
cities_list = ['Baltata', 'Balti', 'Bravicea', 'Briceni', 'Cahul', 'Camenca',
               'Ceadir-Lunga', 'Chisinau', 'Codrii', 'Comrat', 'Cornesti',
               'Dubasari', 'Falesti', 'Leova', 'Ribnita', 'Soroca', 'Stefan-Voda', 'Tiraspol']
cities = '\n'.join(cities_list)

def Temp(city):
    opener = urllib.request.URLopener({})

    url = "http://old.meteo.md/"

    f = opener.open(url)
    content = f.read()
    soup = bs(content, "lxml")

    p_class = soup.findAll('p', align="right")
    p_class = list(p_class)
    strings = []
    for x in p_class:
        strings.append(str(x))

    main_string = [s for s in strings if city in s]

    res = re.search('<br/> (.*)</font', main_string[0])

    return res.group(1)

def console(message, answer):
    print("\n~~~~~~~~~~~~~~~")
    print(datetime.now())
    print('Message from {}: {}. Answer: {}. ID: {}.'.format(
        message.from_user.first_name, message.text, answer, str(message.from_user.id)))


@TelegramBot.message_handler(commands=['flag'])
def handle_text(message):
    console(message, 'Flag')
    TelegramBot.send_message(message.chat.id, '💙💛❤')

@TelegramBot.message_handler(commands=['cities'])
def handle_text(message):
    console(message, 'Cities')
    TelegramBot.send_message(message.chat.id, cities)

@TelegramBot.message_handler(commands=['start'])
def handle_text(message):
    console(message, 'Start')
    buttons = telebot.types.ReplyKeyboardMarkup(True)
    buttons.row('Chisinau', 'Balti', 'Comrat')
    buttons.row('Falesti', 'Soroca', 'Cahul')

    TelegramBot.send_message(message.chat.id, '''Choose city from below or type it's name''', reply_markup=buttons)

@TelegramBot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        temperature = Temp(str(message.text))
    except:
        TelegramBot.send_message(message.chat.id, "No information about this city")
        console(message, "No info")
        return

    result = "Temperature in {} is {}°C".format(message.text, temperature)
    console(message, temperature)
    TelegramBot.send_message(message.chat.id, result)

TelegramBot.polling(none_stop=True, interval=0)


