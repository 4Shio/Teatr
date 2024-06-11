from sqlalchemy import text
from alchemybase import engine,Speki
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
import requests
import asyncio
import asyncio
from aiogram import *
from aiogram.filters import Command 
from aiogram.types import *
from aiogram.utils.keyboard import ReplyKeyboardBuilder
symvols_to_delete = "/"

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

                    with Session(engine) as session:
                        if session.query(Speki).filter_by(name = tit , date = datesp, time = timesp).count() == 0:
                            spek = Speki(name = tit, date = datesp,time = timesp, info = info)
                            session.add(spek)
                            session.commit()
                except Exception as ex:
                    print(ex)
        except:
            pass
        
    print('Update complete')
    await asyncio.sleep(1000)

bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
dp = Dispatcher()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


remove_key = ReplyKeyboardRemove()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота", reply_markup=make_row_keyboard(["View", "LAfterT","analys","Next"] ))

@dp.message(F.text == "View")
async def view(message: types.Message):
    pass
async def main():
    task = asyncio.create_task(update)
    task2 = asyncio.create_task(dp.start_polling(bot))
    await task
    await task2
if __name__ == "__main__":
    asyncio.run(main())

    