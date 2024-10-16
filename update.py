from bs4 import BeautifulSoup
import requests
from base import Speki
from sqlalchemy import func,select,delete
from func import pages,replace,week_list,del_s,date_repp
from datetime import datetime
import asyncio
from config import async_session
async def update():
    while True:
        print("Update begin")
        async with async_session() as session:
            
            deleleter  = delete(Speki).where(Speki.date > datetime.now())
            await session.execute(deleleter)
            await session.commit()
                
        for i in pages:
            
            page = requests.get(i)
            soup = BeautifulSoup(page.text, "html.parser")
            spectacless = (soup.find_all(class_='AffichesItem_item__NUTcg'))
            
            for iow, el in enumerate(spectacless):
                try:
                    under_name = el.find(class_="AffichesItem_stage__W7j3k").text
                    
                    if under_name != None:
                        if under_name in ['Открытие балетного сезона','Малая сцена','Открытие оперного сезона','Фестиваль молодых звезд оперы «Опера Vita»']:
                            pass
                        
                        else:
                            continue
                except:
                    pass
                #Число и дата
                datesp= replace((str(el.find(class_='AffichesItem_date__tJDVL').text)))
                timesp = str(el.find(class_='AffichesItem_time__Kffzs').text)
                    
                full_date_d = date_repp(( str(datetime.now().year)  + "-" + datesp.split('-')[1] + '-' +datesp.split('-')[0] + " " + timesp.split(',')[0]))
                
                if full_date_d < datetime.now():
                    full_date_d = date_repp(( str(int(datetime.now().year)+1)  + "-" + datesp.split('-')[1] + '-' +datesp.split('-')[0] + " " + timesp.split(',')[0]))
                
                weekday =week_list.get(del_s(timesp.split(',')[1]))
                # Название
                tit = str(el.find(class_='AffichesItem_title__1rN_h').text)
                
                # Длительность
                info = (el.find(class_='AffichesItem_centerLeft__DYkLc').text)

                async with async_session() as session:
                    count = await session.execute(select(func.count(Speki.date)).where(Speki.date ==full_date_d and Speki.name ==tit))
                    s_count = count.scalar()
                    if s_count == 0:
                        spek = Speki(name = tit, 
                                         date = full_date_d,
                                         info = info,
                                         weekday = weekday)
                                     
                        session.add(spek)
                        await session.commit()
                    
        print('Update complete', datetime.now())
        await asyncio.sleep(100000)
