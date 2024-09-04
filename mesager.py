from base import user,Speki
from config import async_session
from datetime import *
from config import tg_token
from aiogram import Bot
from sqlalchemy import select,func
bot = Bot(tg_token)

async def mesager():
        try:
            async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
                time_untill = first_date  - datetime.now()
                if time_untill == timedelta(days=1,hours=0):
                    print('Work')
                    stmts = select(user.id)
                    id_tg = await session.scalar(stmts)
                    bot.send_message(chat_id=id_tg ,text='Time to work')
        except Exception as ex:
            print(ex)
            
            
            
            
            
            
            