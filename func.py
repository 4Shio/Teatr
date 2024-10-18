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
month_list = {
"01":"Января",
"02":"Февраля",
"03":"Марта",
"04":"Апреля",
"05":"Мая",
"06":"Июня",
"07":"Июля",
"08":"Августа",
"09":"Сентября",
"10":"Октября",
"11":"Ноября",
"12":"Декабря"
}

symvols_to_delete = "/"

space_del = " "

pages = ["https://mrteatr.ru/afisha/?page=1", "https://mrteatr.ru/afisha/?page=2", "https://mrteatr.ru/afisha/?page=3"]

def replace(data):
    for sym in symvols_to_delete:
                  return data.replace(sym,"-")
    

def date_repp(date):
        #print((datetime.strptime((date),"%Y-%m-%d %H:%M:%S")))
        return datetime.strptime((date),"%Y-%m-%d %H:%M")
              
def date_rep(date):
        return datetime.strftime(date_repp(date),"%Y-%m-%d %H:%M")

def del_s(var):
        for i in space_del:
                return var.replace(i,'')
        
def format(value,type):
    messages =''
    if type == 'one':
    
        return  (messages + 
                                str(value[0]) + #name
                                "\n"  + str(value[1]) + #weekday
                                ' ' + str(datetime.strftime(value[2],'%d')) + # Day
                                " " + str(month_list.get(datetime.strftime(value[2],'%m')))  + #Month
                                " " +  str(datetime.strftime(value[2],'%H:%M')) +"\n" + #time
                                str(value[3]) +'\n' +'\n') #Info

    else:
        for i in value:
                try:
                    messages = (messages + 
                                str(i[0]) + #name
                                "\n"  + str(i[1]) + #weekday
                                ' ' + str(datetime.strftime(i[2],'%d')) + # Day
                                " " + str(month_list.get(datetime.strftime(i[2],'%m')))  + #Month
                                " " +  str(datetime.strftime(i[2],'%H:%M')) +"\n" + #time
                                str(i[3]) +'\n' +'\n') #Info
                except Exception as ex:
                    print(ex)
                    
    return messages
