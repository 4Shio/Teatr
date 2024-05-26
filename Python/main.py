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


connection , cursor = get_connection()
now = datetime.now()
today = now.strftime("%d %m")
bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')

symvols_to_delete = "/"
dp = Dispatcher()


def datechek(date):
    if (datetime.strptime(date,"%d %m")) > (datetime.strptime(today,"%d %m")):
        return 1
    else:
        return 0


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


remove_key = ReplyKeyboardRemove()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота", reply_markup=make_row_keyboard(["View", "LAfterT","analys"] ))

@dp.message(F.text == "View")
async def view(message: types.Message):
    await message.answer( text = '\n'.join(' '.join (str(i) for i in v ) for v in fetchall("SELECT name, date, time FROM test")))

@dp.message(F.text == "Add")
async def Del(message: types.Message):
    await message.answer(text='')
    
@dp.message(F.text == "analys")
async def analys(message: types.Message):
    await message.answer(text='\n'.join(' '.join (str(i) for i in v ) for v in fetchall("SELECT name, turns FROM analys")))

@dp.message(F.text == "LAfterT")
async def LAfrerT(message: types.Message):
    await message.answer(text='\n'.join(' '.join (str(i) for i in v ) for v in fetchall("SELECT name, date, time FROM test WHERE aftday =%s",([1]))))
                                
                         
                        


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
                    #if (datetime.strptime(timesp,"%d %m"))> (datetime.strptime(today,"%d %m")):
                     #   print("da")
                    if fetchone("SELECT COUNT(*) FROM test WHERE name =%s AND date = %s",(tit,datesp)) == 0:
                         
                        change_data("INSERT INTO TEST (date, name, time, info, aftday ) VALUES (%s ,%s ,%s, %s, %s)", (datesp, tit, timesp, info, datechek(datesp)))
                   
                except Exception as ex:
                    print(ex)
        except:
            pass
        

        
    print('Update complete')
    #try:
     #   dates = fetchall("SELECT date FROM test")
      #  for i,e in enumerate (dates):
       #     if (datetime.strptime(dates[i][0],'%d %m')) > datetime.strptime(today,"%d %m"):
        #        change_data("INSERT INTO TEST (aftday)  (%s)",(1))
         #       #print(fetchall("SELECT name ,date ,time FROM test WHERE date = %s",(dates[i])))
    #except Exception as ex:
    #   print(ex)
           


    
    

    try:
        names = fetchall("SELECT name FROM test") 
        for i,e in enumerate (names):
            if fetchone("SELECT COUNT(*) FROM analys WHERE name = %s",(names[i])) == 0:
                change_data("INSERT INTO analys (name, turns) VALUES (%s,%s)", (names[i][0],fetchone(" SELECT COUNT(*) FROM test WHERE name =%s",(names[i]))))  
        
        print("Analys complete")
    except Exception as ex:
        print(ex)
    await asyncio.sleep(1000)       

       


async def main():
    task1 = asyncio.create_task(update())
    task2 = asyncio.create_task(dp.start_polling(bot))
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())
