import datetime
import time
import bs4
from bs4 import BeautifulSoup
import requests
from datetime import *
import asyncio
import aiogram
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message


now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
speki = {}
dp = Dispatcher()

async def command_start(message:Message) -> None:
    await message.answer(f"Привет от бота ")

@dp.message()
async def echo_handler(message: types.Message) -> None:
    if message.text == "Следующий спектакль":
        spek = ' '.join(str(i) for i in speki[0])
        await bot.send_message(chat_id=message.chat.id, text=f"{spek}")
    if message.text == "Список всех следующих спектаклей":
        spekt = '\n'.join(' '.join(str(i) for i in v) for v in speki.values())
        await bot.send_message(chat_id=message.chat.id, text=f"{spekt}")

async def update():

    url = 'https://mrteatr.ru/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    spectacless = soup.find_all(class_='item')
    months = {'октября': 10, 'ноября': 11, 'декабря': 12, 'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
                  'мая': 5,
                  'июня': 6, 'июля': 7, 'сентября': 9}
    for i, el in enumerate(spectacless):
            try:
                timesp = el.find(class_='time').text.split()
                tit = el.find('a').text
                speki[i] = [timesp[0], timesp[1], months[timesp[1]], timesp[3], tit]
            except:
                pass


async def main():
    while True:
        task1 = asyncio.create_task(update())
        task2 = asyncio.create_task(dp.start_polling(bot))
        await  task1
        await task2





if __name__ == "__main__":

    asyncio.run(main())
    print(speki[0])
