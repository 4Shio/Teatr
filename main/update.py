from bs4 import BeautifulSoup
import requests
from base import *
from func import pages,symvols_to_delete,replace,date_rep,week_list,del_s
import time

def update():
    print("Update begin")
    for i in pages:
        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.text, "html.parser")
            spectacless = (soup.find_all(class_='AffichesItem_item__NUTcg'))
            for iow, el in enumerate(spectacless):
                try:
                    # Число и дата
                    datesp = str(el.find(class_='AffichesItem_date__tJDVL').text)
                    datesp= replace(datesp)
                    
                    # Время
                    timesp = str(el.find(class_='AffichesItem_time__Kffzs').text)
                    
                    full_date =date_rep(( str(datetime.now().year)  + "-" + datesp.split('-')[1] + '-' +datesp.split('-')[0] + " " + timesp.split(',')[0] + ':'+str(0)+str(0)))
                    
                    weekday =  timesp.split(',')[1]
                    weekday =week_list.get(del_s(weekday))
                    
                    # Название
                    tit = str(el.find(class_='AffichesItem_title__1rN_h').text)
                    # Длительность
                    info = str(el.find(class_='AffichesItem_centerLeft__DYkLc').text)

                    if (session.query(Speki).filter_by(name = tit, date = full_date , time = full_date, weekday = weekday).count()) == 0:
                        spek = Speki(name = tit, date = full_date,time = full_date,info = info, weekday = weekday)
                        session.add(spek)

                except Exception as ex:
                    print(ex)
        except:
            pass
        
    session.commit()
    print('Update complete')
    time.sleep(1000)