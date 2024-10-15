from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from base import Speki,user
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
from datetime import *
from aiogram.fsm.state import StatesGroup, State
from config import async_session
from sqlalchemy import select,func
from func import month_list
now = datetime.now()

router = Router()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row],one_time_keyboard = True)

remove_key = ReplyKeyboardRemove()

def make_str(text_str):
    return   ' '.join(str(i) for i in text_str )

def make_more_str(text_str):
      return '\n'.join(' \n'.join(str(i) for i in v) for v in text_str)

async def get_from_db(value,stmt):
    async with async_session() as session:
        if value == 'all':
            return (await session.scalars(stmt)).all() 
        
        if value == 'one':
            messages =''
            i = (await session.execute(stmt)).first()
            messages = (messages + 
                                str(i[0]) + #name
                                "\n"  + str(i[1]) + #weekday
                                ' ' + str(datetime.strftime(i[2],'%d')) + # Day
                                " " + str(month_list.get(datetime.strftime(i[2],'%m')))  + #Month
                                " " +  str(datetime.strftime(i[2],'%H:%M')) +"\n" + #time
                                str(i[3]) +'\n' +'\n') #Info           
            return messages
                
        if value =="alle":
            
            return format((await session.execute(stmt)).all())
        
        
def format(value):
    messages =''
    for el,i in enumerate(value):
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
    


    
@router.message(Command("start"))
async def start(message:Message):
                await message.answer(text='Приветсвую - это неофициальный бот музыкального театра для просмотра расписания',reply_markup=make_row_keyboard(["Все следующие","Следующий","На неделю"]))


@router.message(F.text == 'Все следующие')
async def get_all(message_get_all:Message):
        
    test = ((await get_from_db('alle',select(Speki.name,Speki.weekday,Speki.date,Speki.info).where(Speki.date > datetime.now()).order_by(Speki.date))))
    await message_get_all.answer(text=test)
    
    
@router.message(F.text == "На неделю")
async def get_week(message_wwek:Message):
        
    result =(await get_from_db('alle',select(Speki.name,Speki.weekday,Speki.date,Speki.info).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=6))).order_by(Speki.date)))
    await message_wwek.answer(result)
      

@router.message(F.text == 'Следующий')
async def get_all(message_get_one:Message):
    
    result = (await get_from_db('one',select(Speki.name,Speki.weekday,Speki.date,Speki.info).where(Speki.date > datetime.now()).order_by(Speki.date)))
    await message_get_one.answer(text= result)
        
   

@router.message(Command('op'))
async def adm(m_adm:Message):
    async with async_session() as session:
        
        admin = 'Admin'
        stmt = select(func.count(user.t_id)).where(user.role == admin and user.t_id== m_adm.from_user.id)
        chek = await session.scalar(stmt)
        if chek ==0:
            n_adm = user(name = m_adm.from_user.full_name,
                         t_id = m_adm.from_user.id,
                         role = admin,
                         note = False)
            session.add(n_adm)
        else:print("Alredy in use")
        await session.commit()
        await session.close()

@router.message(Command('not'))
async def adm(m_not:Message):
    async with async_session() as session:
        
        
        chek = (await get_from_db(select(func.count(user.id)).where(user.role == 'user' and user.t_id == m_not.from_user.id == user.t_id))).all()
        if chek ==0:
            n_note = user(name = m_not.from_user.full_name,
                         t_id = m_not.from_user.id,
                         role = 'user',
                         note = True)
            session.add(n_note)
            await session.commit()
            await session.close()
        else:
            print("Alredy in use")
          
        await session.commit()
        await session.close()

@router.message(Command('get_users'))
async def test_notes(test_not:Message):
    async with async_session() as session:
       users = (await session.execute(select(user.t_id).where(user.note == True))).scalars()
        #users =  await get_users()
    try:
        for i in users:
            print(i)
            test_not.answer(text= str(i))
    except Exception as ex:
        print(ex)