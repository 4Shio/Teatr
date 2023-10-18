import datetime
import telebot
import bs4
from bs4 import BeautifulSoup
import requests
from telebot import types
from datetime import *
import asyncio

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
speki = {}
vrem = {}
spectacless = soup.find_all(class_='item')
months = {'октября': 10, 'ноября': 11, 'декабря': 12, 'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5,
          'июня': 6, 'июля': 7, 'сентября': 9}


#print(vrem[0][-4],vrem[0][-3],vrem[0][-2],vrem[0][-1])
for i, el in enumerate(spectacless):
    try:

        timesp = el.find(class_='time').text.split()
        tit = el.find('a').text
        vrem = (el.find('p').text).split()
        speki[i] = [timesp[0], timesp[1], months[timesp[1]], timesp[3], tit]

    except:
        pass
print(speki[0][2])
# 19 октября среда 18:00

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Следующий спектакль"):
        date = datetime.datetime(year=now.year, month=speki[0][2], day=speki[0][0])
        if (now.day - timedelta(days=2)) == date.day and date.month == now.month:
            bot.send_message(message.chat.id, text=f'Завта в {speki[0][3]} будет {speki[0][4]}\n Приходить к {speki[0][3]-timedelta(hours=1)}')
        bot.send_message(message.chat.id, text=f"{speki[0]}")

    if (message.text == "Список всех следующих спектаклей"):
        for i in speki:
            bot.send_message(message.chat.id,text=f'{speki[i]}\n')
    #if (message.text == "Найти определённый спектакль"):
     #   a = telebot.types.ReplyKeyboardRemove()
      #  bot.send_message(message.from_user.id, 'Выберите нужный вам спектакль', reply_markup=a)



bot.infinity_polling()
