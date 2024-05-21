from bs4 import BeautifulSoup
import requests
from datetime import *
import asyncio
from aiogram import *
from aiogram.filters import Command 
from aiogram.types import *
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import user, host, password, db_name
from sql import change_data, fetchall, fetchone, get_connection



now = datetime.now()
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')

symvols_to_delete = "/"
dp = Dispatcher()
        


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


remove_key = ReplyKeyboardRemove()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота", reply_markup=make_row_keyboard(["View", "Add"] ))

@dp.message(F.text == "View")
async def view(message: types.Message):
    await message.answer( text = '\n'.join(' '.join (str(i) for i in v ) for v in fetchall("SELECT name, date, time FROM test")))

@dp.message(F.text == "Add")
async def Del(message: types.Message):
    await message.answer(text='')
   

pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2", "https://mrteatr.ru/afisha/?page=3",
         "https://mrteatr.ru/afisha/?page=4"]

tupel = []


async def update():
    
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
                    
                    if fetchone("SELECT COUNT(*) FROM test WHERE name =%s AND date = %s",(tit,datesp)) == 0:
                        change_data("INSERT INTO TEST (date, name, time, info ) VALUES (%s ,%s ,%s, %s)", (datesp, tit, timesp, info))
                    
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
