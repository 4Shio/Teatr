from base import user,Speki
from config import async_session
from datetime import *
from config import tg_token
from aiogram import Bot
from sqlalchemy import select
from  func import format
import asyncio
from func import month_list
bot = Bot(tg_token)


async def get_first_date():
    async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
    return first_date                
     

async def get_name_of_first():
    return await get_from_db('one',select(Speki.name,Speki.weekday,Speki.date,Speki.info).where(Speki.date > datetime.now()).order_by(Speki.date),'None')

async def get_users():
    return  await get_from_db('all',select(user.t_id).where(user.note == True),'None')

async def get_from_db(value,stmt,type):
    async with async_session() as session:
        if type == None:
            type = 'None'
        if value == 'all':
            return (await session.scalars(stmt)).all() 
        
        if value == 'one':
            return(format((await session.execute(stmt)).fetchone(),'one'))
                
        if value =="alle":
            
            return format((await session.execute(stmt)).all(),type)
        
        


async def today_notes():
    await asyncio.sleep(10)
    while True:

         first_date = await get_first_date()
         if datetime.now().date() == first_date.date() and datetime.now().hour == 8:
             next_one = await get_name_of_first()
             users = await get_users()
             for i in users:
                 await bot.send_message(chat_id=i,text=next_one)
             await asyncio.sleep(3700)
                   
                   
async def tommorow_notes():
    await asyncio.sleep(10)
    while True:

        first_date = await get_first_date()

        if (first_date.date() - timedelta(days=1)) == datetime.now().date() and datetime.now().hour == 8:

            users = await get_users()
            next_one = await get_name_of_first()

            for i in users:
                await bot.send_message(chat_id=i ,text = next_one)
            await asyncio.sleep(3700)
                    
                    
                
                
async def week_notes():
    await asyncio.sleep(10)
    while True:
        if datetime.now().weekday() == 0 and datetime.now().hour == 8:
            users = await get_users()
            next_week = (await get_from_db('alle',select(Speki.name,Speki.weekday,Speki.date,Speki.info).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=6))).order_by(Speki.date),'None'))
            
            for i in users:
                await bot.send_message(chat_id=i,text = next_week)
                
        await asyncio.sleep(3700)
        
            
            
            
            
            