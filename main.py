import datetime
import string
from shlex import join
import telebot
import bs4
from bs4 import BeautifulSoup
import requests
from telebot import types
from datetime import *
import time
import re
import pandas
now = datetime.now()
id = [551057845, 1080107997, 6386209825, 402783140]
bot = telebot.TeleBot('6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Следующий спектакль")
    btn1 = types.KeyboardButton("Список всех следующих спектаклей")
    markup.add(btn, btn1)
    bot.send_message(message.chat.id, text='Привет от бота', reply_markup=markup)
url = 'https://mrteatr.ru/'
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
now = datetime.now()
time_str = soup.find(class_='item').find(class_='time').text
title = soup.find(class_='item').find('a').text
monthstr = string
monthint = 0
tabl = pandas.DataFrame
spectacless = soup.find_all(class_='item')
datasp =0
while True:
    for spectaclel in spectacless:
        
        timesp = spectaclel.find(class_='time').text
        tit = spectaclel.find('a').text
        if list(timesp)[3] =='о'or list(timesp)[2] == 'о':
            monthstr = 'Октябрь'
            monthint = 10
        if list(timesp)[3]=='н' or list(timesp)[2]=='н' and list(timesp)[4]=='о':
            monthstr= 'Ноябрь'
            monthint = 11
        if list(timesp)[3] =='д'or list(timesp)[2] =='д':
            monthstr = 'Декабрь'
            monthint = 12
        if list(timesp)[3]=='я'or list(timesp)[2]=='я':
            monthstr= 'Январь'
            monthint = 1
        if list(timesp)[3] =='ф'or list(timesp)[2] == 'ф':
            monthstr = 'Февраль'
            monthint = 2
        if list(timesp)[3]=='м' or list(timesp)[2]=='н' and (list(timesp)[5]=='р'or list(timesp)[4]=='р'):
            monthstr= 'Март'
            monthint = 3
        if list(timesp)[3] =='а'or list(timesp)[2] =='а':
            monthstr = 'Апрель'
            monthint = 4
        if list(timesp)[3]=='м' or list(timesp)[2]=='н' and (list(timesp)[5]=='й'or list(timesp)[4]=='й'):
            monthstr= 'Май'
            monthint = 5
        day = list(timesp)[0] + join(list(timesp)[1])
        tabl = ({'day': [day],'month':[monthstr],'monthi':[monthint], 'Spec': [tit]})
        print(tabl)
    time.sleep(60)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Следующий спектакль"):
        time_str = soup.find(class_='item').find(class_='time').text
        title = soup.find(class_='item').find('a').text
        bot.send_message(message.chat.id, text=f"{time_str}\n{title}")
    if (message.text == "Список всех следующих спектаклей"):
        spectacles = soup.find_all(class_='item')
        for spectacle in spectacles:
            time = spectacle.find(class_='time').text
            titles = spectacle.find('a').text
            bot.send_message(message.chat.id, text=f"{time}\n{titles}")


bot.infinity_polling()
