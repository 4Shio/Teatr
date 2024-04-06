from aiogram.filters import Command
from bs4 import BeautifulSoup
import requests
from datetime import *
import asyncio
from aiogram import *
from aiogram.types import *
import mysql.connector
import logging
from aiogram.utils.keyboard import *
from config import user, host, password, db_name

now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')

symvols_to_delete = "/"

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=3306,
        database=db_name,

    )
    print('Connection complet')
except Exception as ex:
    print(ex)


def get_connection():
    conection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=3306,
        database=db_name)

    cursor = conection.cursor(buffered=True)

    return conection, cursor


def change_data(query, value=None) -> None:
    connection, cursor = get_connection()
    if value is None:
        cursor.execute(query)
        connection.commit()
    else:
        cursor.execute(query, value)
        connection.commit()

    if connection.is_connected():
        connection.close()


def create_if_not_exists() -> None:
    try:
        connection, cursor = get_connection()

        cursor.execute("""CREATE TABLE IF NOT EXISTS TEST (
            date VARCHAR(255),
            name VARCHAR(255),
            time VARCHAR(255),
            info VARCHAR(255)
            
           )""")

        connection.commit()

    except Exception as error_code:
        print("Error Base -> ", error_code)
        connection.close()
    finally:
        connection.close()


async def fetchone(query, value=None):
    connection, cursor = await get_connection()
    if value is None:
        cursor.execute(query)
    else:
        cursor.execute(query, value)

    result = cursor.fetchone()

    if connection.is_connected():
        connection.close()

    return result[0]


async def fetchall(query, value=None):
    connection, cursor = await get_connection()
    if value is None:
        cursor.execute(query)
    else:
        cursor.execute(query, value)

    result = cursor.fetchall()

    if connection.is_connected():
        connection.close()

    return result
create_if_not_exists()
dp = Dispatcher()


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


remove_key = ReplyKeyboardRemove()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота", reply_markup=make_row_keyboard(["View"]))


@dp.message(F.text == "View")
async def view(message: types.Message):
    await message.answer( text = update() )


pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2", "https://mrteatr.ru/afisha/?page=3",
         "https://mrteatr.ru/afisha/?page=4"]

tupel = []


async def update():
    change_data('DELETE FROM TEST ')
    for i in pages:
        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.text, "html.parser")
            spectacless = (soup.find_all(class_='AffichesItem_item__NUTcg'))
            for iow, el in enumerate(spectacless):
                try:

                    # Число и дата
                    datesp = el.find(class_='AffichesItem_date__tJDVL').text

                    for sym in symvols_to_delete:
                        datesp = datesp.replace(sym," ")

                    # Время
                    timesp = str(el.find(class_='AffichesItem_time__Kffzs').text)

                    # Название
                    tit = str(el.find(class_='AffichesItem_title__1rN_h').text)

                    # Длительность
                    info = str(el.find(class_='AffichesItem_centerLeft__DYkLc').text)




                    #Закидывание в базу
                    change_data("INSERT INTO TEST (date, name, time, info) VALUES (%s ,%s ,%s, %s)", (datesp, tit, timesp, info))

                except Exception as ex:
                    print(ex)

        except:
            pass
    print('Update complete')
    await asyncio.sleep(1000)


async def main():
    while True:
        task1 = asyncio.create_task(update())
        task2 = asyncio.create_task(dp.start_polling(bot))
        await task1
        await task2


if __name__ == "__main__":
    asyncio.run(main())
