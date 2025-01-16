from base import user,Speki
from config import async_session
from datetime import *
from config import tg_token
from aiogram import Bot
from sqlalchemy import select
from  func import format
import asyncio

bot = Bot(tg_token)


async def get_first_date():
    async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
    return first_date                
     

async def get_name_of_first():
    async with async_session() as session:
        stmt = select(Speki.name,Speki.weekday,Speki.date,Speki.info).where(Speki.date > datetime.now()).order_by(Speki.date)

        test = await session.scalar(stmt)

    return  format(test)

async def get_users():
    async with async_session() as session:
        
        stmt = select(user.t_id).where(user.note == True)
        users = await  session.scalars(stmt)
    return  users


                


async def today_notes():
    await asyncio.sleep(10)
    while True:

        first_date = await get_first_date()
        
        if datetime.now().date() == first_date.date() and datetime.now().hour == 8 and datetime.now().weekday() !=0 and datetime.now().minute == 0:
             
            next_one = await get_name_of_first()
            users = await get_users()
            
            for i in users:
                
                 await bot.send_message(chat_id=i,text= 'Сегодня' + '\n' + next_one)
            await asyncio.sleep(3700)
            
        if  datetime.now().date() == first_date.date() and datetime.now().hour == (first_date - timedelta(hours = 2)).hour:
            next_one = await get_name_of_first()
            users = await get_users()
             
            for i in users:
                 
                 await bot.send_message(chat_id=i, text =(f"Сегодня \n {next_one}"))
            await asyncio.sleep(3700)
        await asyncio.sleep(10)
                   
                   
async def tommorow_notes():
    await asyncio.sleep(10)
    while True:

        first_date = await get_first_date()

        if (first_date.date() - timedelta(days=1)) == datetime.now().date() and datetime.now().hour == 8 and datetime.now().weekday() != 0:

            users = await get_users()
            next_one = await get_name_of_first()

            for i in users:
                await bot.send_message(chat_id=i ,text =(f"Завтра \n {next_one}"))
            await asyncio.sleep(3700)
        await asyncio.sleep(10)    
                    
                
                
async def week_notes():
    async with async_session() as session:
        
        await asyncio.sleep(20)
        while True:

            if datetime.now().weekday() == 0 and datetime.now().hour == 8:
                users = await get_users()
                stmt = select(Speki.name,Speki.weekday,Speki.date,Speki.info).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=7))).order_by(Speki.date)
                not_format_result = (await session.execute(stmt)).all()

                next_week = format(not_format_result)

                for i in users:
                    await bot.send_message(chat_id=i,text = next_week)

                await asyncio.sleep(3700)
            await asyncio.sleep(10)