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
import logging
from aiogram.utils.keyboard import *
builder = ReplyKeyboardBuilder()
chek = False
now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
speki = {}
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



def raspisanieq():
    builder.button(text='Следующий спектакль')
    builder.button(text='Список всех следующих спектаклей')
    builder.button(text='Добавить спектакль')
    builder.button(text='В меню')
    return builder.as_markup()
def account():
    types.ReplyKeyboardRemove
    builder.button(text='Включить уведомления')
    builder.button(text='Выключить уведомления')
    builder.button(text='Редактировать имя')
    builder.button(text='Удалить аккаунт из базы')
    builder.button(text='В меню')
    return  builder.as_markup(resize_keyboard=True)

def menueq():
    types.ReplyKeyboardRemove
    builder.button(text='Расписание')
    builder.button(text='Натройки аккаунта')
    return  builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота", reply_markup=raspisanieq())
@dp.message(F.text)
async def message(message:types.Message):

    if message.text == "В меню":
        print(123)
        await bot.send_message(chat_id=message.chat.id,text='В меню',reply_markup= menueq())

    if message.text == "Расписание":
        print(321)
        await bot.send_message(chat_id=message.chat.id,text='Расписание',reply_markup= raspisanieq())

    if message.text == "Следующий спектакль":
        cursor.execute("SELECT * FROM Spektakli")
        await bot.send_message(chat_id=message.chat.id, text=' '.join(str(i) for i in cursor.fetchall()[0]))

    if message.text == "Список всех следующих спектаклей":
        cursor.execute("SELECT * FROM Spektakli")
        await bot.send_message(chat_id=message.chat.id, text='\n'.join(' '.join(str(i) for i in v) for v in cursor.fetchall()))

    if message.text == "Настройки аккаунта":
        await bot.send_message(chat_id=message.chat.id, text='Перевожу',reply_markup=account())




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
    await asyncio.sleep(10000)


async def main():
    while True:
        task1 = asyncio.create_task(update())
        task2 = asyncio.create_task(dp.start_polling(bot))
        await task1
        await task2


if __name__ == "__main__":
    asyncio.run(main())
