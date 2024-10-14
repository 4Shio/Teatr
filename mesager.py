from base import user,Speki
from config import async_session
from datetime import *
from config import tg_token
from aiogram import Bot
from sqlalchemy import select,func,update,desc
from handler import make_more_str
import asyncio
bot = Bot(tg_token)


async def get_first_date():
    async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
    return first_date

async def get_name_of_first():
    async with async_session() as session:
        next_one = await session.scalar(select(Speki.message_text).filter(Speki.date > datetime.now()).order_by(Speki.date))        
    return next_one

async def get_users():
    async with async_session() as session:
        users = (await session.execute(select(user.t_id).where(user.note == True))).scalars()
    return users

async def get_from_db(stmt):
    async with async_session() as session:
        return await session.scalars(stmt)

async def today_notes():
    while True:

         first_date = await get_first_date()
         if datetime.now().date() == first_date.date() and datetime.now().hour == 8:
             next_one = await get_name_of_first()
             users = await get_users()
             for i in users:
                 await bot.send_message(chat_id=i,text=next_one)
             await asyncio.sleep(3700)
                   
                   
async def tommorow_notes():
    while True:

        first_date = await get_first_date()

        if (first_date.date() - timedelta(days=1)) == datetime.now().date() and datetime.now().hour == 8:

            users = await get_users()
            next_one = await get_name_of_first()

            for i in users:
                await bot.send_message(chat_id=i ,text = next_one)
            await asyncio.sleep(3700)
                    
                    
                
                
async def week_notes():
    while True:
        if datetime.now().weekday() == 0 and datetime.now().hour == 8:
            
            users = await get_users()
            next_week = (await get_from_db(select(Speki.message_text).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=6))).order_by(Speki.date))).all()
            
           
            try:
                for i in users:
                    await bot.send_message(chat_id=i,text =make_more_str(next_week))
                
            except Exception as ex:
                print(ex)
        await asyncio.sleep(3700)
        
            
            
            
            
            