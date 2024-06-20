from bs4 import BeautifulSoup
import requests
from base import *
import time
import asyncio
pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2", "https://mrteatr.ru/afisha/?page=3",
         "https://mrteatr.ru/afisha/?page=4"]

symvols_to_delete = "/"

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
                    datesp = el.find(class_='AffichesItem_date__tJDVL').text
                    for sym in symvols_to_delete:
                        datesp = datesp.replace(sym," ")
                    # Время
                    timesp = str(el.find(class_='AffichesItem_time__Kffzs').text)
                    # Название
                    tit = str(el.find(class_='AffichesItem_title__1rN_h').text)
                    # Длительность
                    info = str(el.find(class_='AffichesItem_centerLeft__DYkLc').text)

                    if (session.query(Speki).filter_by(name = tit, date = datesp , time = timesp).count()) == 0:
                        
                        spek = Speki(name = tit, date = datesp,time = timesp,info = info)
                        session.add(spek)
                except Exception as ex:
                    print(ex)
        except:
            pass
        
    session.commit()
    print('Update complete')
    time.sleep(1000)