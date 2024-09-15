from base import user,Speki,notes
from config import async_session
from datetime import *
from config import tg_token
from aiogram import Bot
from sqlalchemy import select,func,update
from handler import make_more_str
import asyncio
bot = Bot(tg_token)



async def mesager():
    await asyncio.sleep(10)
    while True:
        try:
            
            async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date).where(Speki.date > datetime.now())
                first_date = await session.scalar(stmt)
                next_one = await   session.scalar(select(Speki.message_text).filter(Speki.date > datetime.now()).order_by(Speki.date))
                
                if (datetime.now() + timedelta(days=1)).date == first_date.date and datetime.now().hour == (first_date.hour - timedelta(hours=2)) :
                    stmts = select(user.t_id).where(user.note == True)
                    id_tg = (await session.execute(stmts)).scalars()
                      
                    for i in id_tg:
                       print(i)
                       await bot.send_message(chat_id=i ,text = next_one)
                    
                    
                if datetime.now().date == first_date.date and datetime.now().hour == first_date.hour - timedelta(hours=2):
                    stmts = select(user.t_id).where(user.note == True)
                    id_tg = (await session.execute(stmts)).scalars()
                      
                    for i in id_tg:
                       print(i)
                       await bot.send_message(chat_id=i ,text = next_one)
                    
                    
                
                
                        
                if datetime.now().weekday() == 0:
                    
                    last_update = await session.scalar(select(notes.date).filter(notes.type == 'week').order_by(notes.date.desc))
                    
                        
                        
                    if last_update.date != datetime.now().date or last_update == None:
                        last_up = notes(date = datetime.now(),type = 'week')
                        await session.add(last_up)
                        await session.commit()
                        
                        
                        
                        next_week_speki = select(Speki.message_text).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=6))).order_by(Speki.date)
                        next_week = (await session.execute(next_week_speki)).all()

                        users = (await session.execute(select(user.t_id).where(user.note == True))).scalars()
                        


                        for i in users:
                            await bot.send_message(chat_id=i,text =make_more_str(next_week))

                    pass
            await session.close()
        except Exception as ex:
            await asyncio.sleep(100)
            print(ex)
            
            
            
            
            
            
            