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
speki ={}
spectacless = soup.find_all(class_='item')
datasp = 0
while True:
    speki.clear()
    for i,el in enumerate(spectacless):
        try:
            timesp = el.find(class_='time').text.split()
            tit = el.find('a').text
            day = list(timesp)[0] + join(list(timesp)[1])
            speki[i]=[timesp[0],timesp[1],timesp[3],tit]
        except:
            pass

    time.sleep(600)
# 19 октября среда 18:00

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Следующий спектакль"):
        time_str = soup.find(class_='item').find(class_='time').text
        title = soup.find(class_='item').find('a').text
        bot.send_message(message.chat.id, text=f"{time_str}\n{title}")

    if (message.text == "Список всех следующих спектаклей"):
        spectacles = soup.find_all(class_='item')
        for spectacle in spectacles:
            try:
                time = spectacle.find(class_='time').text
                titles = spectacle.find('a').text
                bot.send_message(message.chat.id, text=f"{time}\n{titles}")
            except:pass
    if (message.text== "Найти определённый спектакль"):
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Выберите нужный вам спектакль', reply_markup=a)
        @bot.message_handler(content_types=['text'])
        def maese(message):


bot.infinity_polling()
