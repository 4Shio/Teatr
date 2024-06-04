
import psycopg2
from bs4 import BeautifulSoup
import requests
from datetime import*
from alchemy import engine,meta_data,test_table,analys_table
from sqlalchemy import Insert,select,values,func,Table
from sqlalchemy.orm import Session

meta_data.create_all(engine)

now = datetime.now()
today = now.strftime("%d %m")
def datechek(date):
    if (datetime.strptime(date,"%d %m")) > (datetime.strptime(today,"%d %m")):
        return 1
    else:
        return 0

symvols_to_delete = "/"
pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2", "https://mrteatr.ru/afisha/?page=3",
         "https://mrteatr.ru/afisha/?page=4"]
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

                    #Закидывание в базу
                    with engine.connect() as conn:
                        update_base =conn.execute( Insert(test_table).values(
                            [
                                {'name':tit, "date":datesp, "time":timesp,"info":info}
                            ]
                
                    ))
                        conn.commit()
                except Exception as ex:
                    print(ex)
        except:
            pass
        

        
print('Update complete')

