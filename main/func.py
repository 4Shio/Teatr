from datetime import*
now = datetime.now()
year = str(now.year)

week_list = {"пн":"Понедельник",
             "вт":"Вторник",
             "ср":"Среда",
             "чт":"Четверг",
             "пт":"Пятница",
             "сб":"Суббота",
             "вс":"Восскресенье",
             }


symvols_to_delete = "/"

space_del = " "

pages = ["https://mrteatr.ru/afisha/", "https://mrteatr.ru/afisha/?page=2", "https://mrteatr.ru/afisha/?page=3",
         "https://mrteatr.ru/afisha/?page=4"]

def replace(data):
    for sym in symvols_to_delete:
                  return data.replace(sym,"-")
    

def date_repp(date):
        return datetime.strptime((date),"%Y-%m-%d %H:%M:%S")
              
def date_rep(date):
        return datetime.strftime(date_repp(date),"%Y-%m-%d %H:%M:%S")

def del_s(var):
        for i in space_del:
                return var.replace(i,'')
        
def make_str(text_str):
    return   ' '.join(str(i) for i in text_str )

def make_more_str(text_str):
      return '\n'.join('  '.join(str(i) for i in v) for v in text_str)
