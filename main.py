import datetime
import bs4
from aiogram.filters import Command
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
chek = False
now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
speki = []
dp = Dispatcher()

months = {'октября': 10, 'ноября': 11, 'декабря': 12, 'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
                      'мая': 5,
                      'июня': 6, 'июля': 7, 'сентября': 9}




spekti = pd.DataFrame.columns['date', 'name', 'time','antrakt']
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота")

pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2" , "https://mrteatr.ru/afisha/?page=3"  , "https://mrteatr.ru/afisha/?page=4" ]

async def update():
    masbase = []
    for i in pages:
        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.text, "html.parser")
            print(page)
            spectacless = ( soup.find_all(class_='AffichesItem_item__NUTcg'))


            for iow, el in enumerate(spectacless):
                    try:
                        masbase.append(el.text)
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
                    except:pass
            #print('\n'.join(str(i) for i in v) for v in masbase)
            #print(' '.join(str(i) for i in masbase))
        except:pass

    print('\n'.join(masbase))
    await asyncio.sleep(10000)

#async def update2():
#    spektakli = []
#    for i in pages:
#        #try:
#            url = pages[i]
#            driver.get(url)
#            driver.implicitly_wait(10)
#            spektakli.append( driver.find_elements(By.CLASS_NAME,"AffichesItem_item__NUTcg"))
#            driver.execute_script("arguments[0].scrollIntoView(true);", spektakli[-1])
#       #except Exception as niger:
#       #    print(niger)
#


async def main():
    while True:
        task1 = asyncio.create_task(update())
        task2 = asyncio.create_task(dp.start_polling(bot))
        #task3 = asyncio.create_task(update2())
        await task1
        await task2
        #await task3


if __name__ == "__main__":
    #driver = webdriver.Chrome()
    asyncio.run(main())
