from base import user,Speki
from config import async_session
from datetime import *
from config import tg_token
from aiogram import Bot
from sqlalchemy import select,func,update
bot = Bot(tg_token)

async def mesager():
   # while True:
        try:
            async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
                time_untill = first_date  - datetime.now()
               
                if time_untill == timedelta(days=1,hours=0):
                    
                    print('Work')
                    print((await session.execute(select(user.note))).all())
                    stmts = select(user.t_id).where(user.note == True)
                    id_tg = (await session.execute(stmts)).scalars()
                    for i in id_tg:
                       print(i)
                       await bot.send_message(chat_id=i ,text='Time to work')
                    
                        
                        
                        
                        
                        
                if datetime.now().weekday() == 0:
                    
                    #stmts = select(Speki.name,Speki.date).where(Speki.date > datetime.now() and Speki.date< datetime.now() + timedelta(days=7))
                    #next_week = await session.scalars(stmts)
                    users = (await session.execute(select(user.t_id).where(user.note == True))).scalars()
                    
                    for i in (await session.execute(select(user.note))).scalars():
                        print(i)
                    for i in users:
                        await bot.send_message(chat_id=i,text = 'Full week work')
                    
                    pass
            await session.close()
        except Exception as ex:
            print(ex)
            
            
            
            
            
            
            