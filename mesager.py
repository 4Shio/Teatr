from base import user,Speki,notes
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

async def get_name_of_firt():
    async with async_session() as session:
        next_one = await session.scalar(select(Speki.message_text).filter(Speki.date > datetime.now()).order_by(Speki.date))        
    return next_one

async def get_users():
    async with async_session() as session:
        users = (await session.execute(select(user.t_id).where(user.note == True))).scalars()
    return users


async def dayly_notes():
    while True:
            async with async_session() as session:
                
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
                next_one = await session.scalar(select(Speki.message_text).filter(Speki.date > datetime.now()).order_by(Speki.date))
                
               
                if (datetime.now() + timedelta(days=1)).date() == first_date.date() and datetime.now().hour == 12 :
                                          
                    for i in users:
                       print(i)
                       await bot.send_message(chat_id=i ,text = next_one)
                    
                    
                    
                    
                if datetime(datetime.now().strftime("%Y-%m-%d %H")) == (datetime(first_date.strftime("%Y-%m-%d %H")) - timedelta(hours=2)):
                   
                    for i in users:
                       print(i)
                       await bot.send_message(chat_id=i ,text = next_one)
                    
                    
                
                
async def week_notes():
    while True:
        async with async_session() as session:
            if datetime.now().weekday() == 0 and datetime.now().hour == 8:

                users = get_users()

                next_week_speki = select(Speki.message_text).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=6))).order_by(Speki.date)
                next_week = (await session.execute(next_week_speki)).all()
                try:
                    for i in users:
                        await bot.send_message(chat_id=i,text =make_more_str(next_week))
                    last_up = notes(date = datetime.now(), type = 'week')
                    session.add(last_up)
                    await session.commit()
                except Exception as ex:
                    print(ex)
     
            
            
            
            
            
            