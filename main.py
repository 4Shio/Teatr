import datetime
import bs4
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import types, F
from bs4 import BeautifulSoup
import requests
from datetime import *
import asyncio
import aiogram
from aiogram import *
from aiogram.types import *
import numpy as np
#import logging
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from aiogram.utils.keyboard import *
import pandas as pd
builder = ReplyKeyboardBuilder()

now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
speki = {"date":[],
        "time":[],
        "title":[],
        "info":[]}

dp = Dispatcher()



def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


remove_key = ReplyKeyboardRemove()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота",reply_markup=make_row_keyboard(["View"]))

@dp.message(F.text == "View")
async def view(message:types.Message):

    await message.answer(text = update())

pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2" , "https://mrteatr.ru/afisha/?page=3"  , "https://mrteatr.ru/afisha/?page=4" ]


def update():
    for i in pages:
        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.text, "html.parser")
            spectacless = ( soup.find_all(class_='AffichesItem_item__NUTcg'))
            for iow, el in enumerate(spectacless):
                    try:

                        #Число и дата
                        datesp = str(el.find(class_='AffichesItem_date__tJDVL').text)
                        #print (datesp)
                        #Время
                        timesp = str(el.find(class_='AffichesItem_time__Kffzs').text)
                        #print (timesp)
                        #Название
                        tit = str(el.find(class_='AffichesItem_title__1rN_h').text)
                        #print(tit)
                        #Длительность
                        info = str(el.find(class_='AffichesItem_centerLeft__DYkLc').text)
                        #print(info)
                        speki["date"].append(datesp)
                        speki["time"].append(timesp)
                        speki["title"].append(tit)
                        speki["info"].append(info)
                    except:pass

        except:pass
    
    result = " "
    
    for i,eli in enumerate(speki["date"]):
         result = result + " " + speki["date"][i] + " "  + speki["time"][i] + " " + speki["title"][i] + " " + speki["info"][i] + "\n"

    return result
   



async def main():
    await dp.start_polling(bot)
        
if __name__ == "__main__":
    asyncio.run(main())
