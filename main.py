import datetime
import telebot
import bs4
from bs4 import BeautifulSoup
import requests
from telebot import types
from datetime import*
import time
import re
id=[551057845,1080107997,6386209825,402783140]
bot =telebot.TeleBot('6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Следующий спектакль")
    btn1 = types.KeyboardButton("Список всех следующих спектаклей")
    markup.add(btn,btn1)
    bot.send_message(message.chat.id,text='Привет от бота',reply_markup=markup)
url = 'https://mrteatr.ru/'
page = requests.get(url)
soup = BeautifulSoup(page.text,"html.parser")
now = datetime.now()
time_str = soup.find( class_='item').find(class_='time')
title = soup.find(class_='item').find('a').text



@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Следующий спектакль"):
        time_str = soup.find(class_='item').find(class_='time').text
        title = soup.find(class_='item').find('a').text
        bot.send_message(message.chat.id,text=f"{time_str}\n{title}")
    if (message.text == "Список всех следующих спектаклей"):
        spectacles = soup.find_all(class_='item')
        for spectacle in spectacles:
            time = spectacle.find(class_='time').text
            titles = spectacle.find('a').text
            bot.send_message(message.chat.id, text=f"{time}\n{titles}")
    #if(message.text=='RC'):
        #bot.send_message(chat_id=551057845,text='Работает')
        #bot.send_message(chat_id=id[1080107997], text='Работает')
        ##bot.send_message(chat_id=id[3], text='Работает')

bot.infinity_polling()