import datetime
import time
import bs4
from aiogram.filters import Command
from bs4 import BeautifulSoup
import requests
from datetime import *
import asyncio
import aiogram
import sqlite3
from aiogram import *
from aiogram.types import *
chek = False
now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
speki = {}
# spek = {}
link = 0
dp = Dispatcher()
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Spektakli (
            day INTEGER,
            month TEXT NOT NULL,
            months INTEGER,
            time INTEGER,
            name TEXT NOT NULL,
            vrem INTEGER
            )
            ''')

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Следующий спектакль")],
        [types.KeyboardButton(text="Список всех следующих спектаклей")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await bot.send_message(chat_id=message.chat.id, text="Привет от бота ", reply_markup=keyboard)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    if message.text == "Следующий спектакль":
        cursor.execute("SELECT * FROM Spektakli")
        await bot.send_message(chat_id=message.chat.id, text=' '.join(str(i) for i in cursor.fetchall()[0]))
    if message.text == "Список всех следующих спектаклей":
        cursor.execute("SELECT * FROM Spektakli")
        spekt = '\n'.join(' '.join(str(i) for i in v) for v in cursor.fetchall())
        await bot.send_message(chat_id=message.chat.id, text=f"{spekt}")


async def update():
    cursor.execute('DELETE FROM Spektakli')
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
            if chek == True:
                if cursor.execute('''SELECT * FROM Spektakli WHERE name = ?''',(tit,)).fetchone() is not None and \
                    cursor.execute('''SELECT * FROM Spektakli WHERE month = ?''', (timesp[1],)).fetchone() is not None and\
                    cursor.execute('''SELECT * FROM Spektakli WHERE day = ?''',(timesp[0],)).fetchone() is not None and \
                    cursor.execute('''SELECT * FROM Spektakli WHERE time = ?''', (timesp[3],)).fetchone() is not None:
                    pass
                else:
                    cursor.execute('INSERT INTO Spektakli (day, month, months, time, name) VALUES (?, ?, ?, ?, ? )',
                               (timesp[0], timesp[1], months[timesp[1]], timesp[3], tit))
                    connection.commit()
            else:
                cursor.execute('INSERT INTO Spektakli (day, month, months, time, name) VALUES (?, ?, ?, ?, ? )',
                               (timesp[0], timesp[1], months[timesp[1]], timesp[3], tit))
                connection.commit()
                chek == True
        except:pass
        connection.commit()
    await asyncio.sleep(10)


async def main():
    while True:
        task1 = asyncio.create_task(update())
        task2 = asyncio.create_task(dp.start_polling(bot))
        await task1
        await task2


if __name__ == "__main__":
    asyncio.run(main())
