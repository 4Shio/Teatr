from bs4 import BeautifulSoup
import requests
from base import *
from sqlalchemy import func
from func import pages,symvols_to_delete,replace,week_list,del_s,month_list,date_repp,date_rep

import re
import asyncio
from aiogram import Bot
bot = Bot(token)
async def update():
    while True:
        print("Update begin")
        for i in pages:
            try:
                page = requests.get(i)
                soup = BeautifulSoup(page.text, "html.parser")
                spectacless = (soup.find_all(class_='AffichesItem_item__NUTcg'))
                for iow, el in enumerate(spectacless):
                    try:
                        # Число и дата
                        datesp= replace((str(el.find(class_='AffichesItem_date__tJDVL').text)))

                        timesp = str(el.find(class_='AffichesItem_time__Kffzs').text)


                        full_date =date_rep(( str(datetime.now().year)  + "-" + datesp.split('-')[1] + '-' +datesp.split('-')[0] + " " + timesp.split(',')[0]))
                        
                        full_date_d = date_repp(( str(datetime.now().year)  + "-" + datesp.split('-')[1] + '-' +datesp.split('-')[0] + " " + timesp.split(',')[0]))

                        weekday =week_list.get(del_s(timesp.split(',')[1]))

                        # Название
                        tit = str(el.find(class_='AffichesItem_title__1rN_h').text)
                        # Длительность
                        info = str(el.find(class_='AffichesItem_centerLeft__DYkLc').text)

                        async with async_session() as session:
                            count = await session.execute(select(func.count(Speki.id)).where(Speki.date ==full_date_d))
                            s_count = count.scalar()
                            if s_count ==0:
                                
                                
                                spek = Speki(name = tit, date = full_date_d,info = info, weekday = weekday,
                                         message_text = tit + "\n" + re.split("-|,|:|,| " , full_date)[2] +" " + 
                                         month_list.get(re.split("-|,|:|,| " , full_date)[1]) + " " + weekday +" "+
                                         re.split("-|,|:|,| " , full_date)[3] +":"+ re.split("-|,|:|,| " , full_date)[4]+ "\n"
                                         + info+" "+"\n"
                                         )
                                session.add(spek)
                                await session.commit()
                    except Exception as ex:
                        print(ex)
            except:
                pass
        
        try:
            stmt = select(user.t_id).where(user.role == 'Admin')
            resul = await session.execute(stmt)
            id = resul.scalar()
            await bot.send_message(chat_id= id,text='Update complete')
        except:
            pass
        await session.commit()
        print('Update complete')
        await asyncio.sleep(1000)
