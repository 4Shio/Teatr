import datetime

import bs4
from bs4 import BeautifulSoup
import requests

from datetime import *
import asyncio
import aiogram
from aiogram import*
from aiogram.filters.command import Command
now = datetime.now()
id = [551057845, 1080107997, 6386209825, 402783140]
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
speki ={}
dp = Dispatcher
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота",reply_markup=markup)

@dp.message('Следующий спектакль')
async def comands(message:types.Message):
    await message.answer("Да")

async def main():
    await dp.start_polling(bot)
    await update()


async def update():
    while True:
        url = 'https://mrteatr.ru/'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        now = datetime.now()
        time_str = soup.find(class_='item').find(class_='time').text
        title = soup.find(class_='item').find('a').text
        spectacless = soup.find_all(class_='item')
        months = {'октября': 10, 'ноября': 11, 'декабря': 12, 'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5,
                  'июня': 6, 'июля': 7, 'сентября': 9}
        for i, el in enumerate(spectacless):
            try:
                timesp = el.find(class_='time').text.split()
                tit = el.find('a').text
                speki[i] = [timesp[0], timesp[1], months[timesp[1]], timesp[3], tit]
            except:
                pass
        print(speki[0][2])




if __name__ == "__main__":
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Следующий спектакль")
    btn1 = types.KeyboardButton("Список всех следующих спектаклей")
    markup.add(btn, btn1)
    asyncio.run(main())
bot.infinity_polling()
