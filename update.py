from bs4 import BeautifulSoup
import requests
from base import *
from func import pages,symvols_to_delete,replace,date_rep,week_list,del_s,month_list
import time
import re
import asyncio
async def update():
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
                    
                    full_date =date_rep(( str(datetime.now().year)  + "-" + datesp.split('-')[1] + '-' +datesp.split('-')[0] + " " + timesp.split(',')[0] + ':'+str(0)+str(0)))
                     
                    weekday =week_list.get(del_s(timesp.split(',')[1]))
                    
                    # Название
                    tit = str(el.find(class_='AffichesItem_title__1rN_h').text)
                    # Длительность
                    info = str(el.find(class_='AffichesItem_centerLeft__DYkLc').text)

                    if (session.query(Speki).filter_by(name = tit, date = full_date ,  weekday = weekday).count()) == 0:
                        spek = Speki(name = tit, date = full_date,info = info, weekday = weekday,
                                     message_text = tit + "\n" + re.split("-|,|:|,| " , full_date)[2] +" " + 
                                     month_list.get(re.split("-|,|:|,| " , full_date)[1]) + " " + weekday +" "+
                                     re.split("-|,|:|,| " , full_date)[3] +":"+ re.split("-|,|:|,| " , full_date)[4]+ "\n"
                                     + info+" "+"\n"
                                     )
                        session.add(spek)

                except Exception as ex:
                    print(ex)
        except:
            pass
        
    session.commit()
    print('Update complete')
    await asyncio.sleep(1000)
    #time.sleep(1000)