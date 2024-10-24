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
from sqlalchemy import select,func,update
from func import format
import calendar
now = datetime.now()

router = Router()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row],one_time_keyboard = True,resize_keyboard=True)

remove_key = ReplyKeyboardRemove()





async def get_from_db(value,type,stmt):
    async with async_session() as session:
        
        if value == 'all':
            if type =='scalar':
                return (await session.scalars(stmt)).all() 
            else:
                return (await session.execute(stmt)).all()
            
        if value == 'one':
            
            if type == 'scalar':
                return await session.scalar(stmt)
            else:
                return (await session.execute(stmt)).fetchone()



@router.message(Command("start"))
async def start(message:Message):
                await message.answer(text=f'Приветствую {message.from_user.full_name}. \n Это бот для просмотра расписания Музыкального театра ',reply_markup=make_row_keyboard(["Следующий","На неделю",'На этот месяц',"Все следующие"]))


@router.message(F.text == 'Все следующие')
async def get_all(message_get_all:Message):
    
    stmt = select(Speki.name,Speki.weekday,Speki.date,Speki.info).where(Speki.date > datetime.now()).order_by(Speki.date).limit(43)
    
    test = format(await get_from_db('all','execute',stmt),'all')
    try:
        await message_get_all.answer(text=test)
    except Exception as ex:
        print(ex)
        await message_get_all.answer('В данный момент эта функция недоступна')


@router.message(F.text == "На неделю")
async def get_week(message_wwek:Message):
    
    stmt = select(Speki.name,Speki.weekday,Speki.date,Speki.info).filter(Speki.date > datetime.now()).filter(Speki.date <= (datetime.now() + timedelta(days=6))).order_by(Speki.date)
    
    test = format(await get_from_db('all','execute',stmt),'all')
    try:
        await message_wwek.answer(text=test)
    except Exception as ex:
        print(ex)
        await message_wwek.answer('В данный момент эта функция недоступна')
        

@router.message(F.text == 'Следующий')
async def get_all(message_get_one:Message):
    
    stmt = select(Speki.name,Speki.weekday,Speki.date,Speki.info).where(Speki.date > datetime.now()).order_by(Speki.date)
    
    test = format(await get_from_db('one','execute',stmt),'one')
    
    try:
        await message_get_one.answer(text= test)
    except Exception as ex:
        print(ex)
        await message_get_one.answer('В данный момент данная функция недоступна')
        
        
@router.message(F.text == 'На этот месяц')
async def get_month(message_month:Message):
    
    last = calendar.monthrange(datetime.now().year, datetime.now().month)
    last_day = datetime.now() + timedelta(days=(last[1] - int(datetime.now().day)))
    
    stmt = select(Speki.name,Speki.weekday,Speki.date,Speki.info).filter(Speki.date > datetime.now()).filter(Speki.date <= last_day).order_by(Speki.date)
    
    result = format(await get_from_db('all','execute',stmt),'all')
    try:
        await message_month.answer(result)   
    except Exception as ex:
        print(ex)
        await message_month.answer('В данный момент данная функция недоступна')
        
        
@router.message(Command('op'))
async def adm(m_adm:Message):
    async with async_session() as session:
        
        admin = 'Admin'
        stmt = select(func.count(user.t_id)).where(user.role == admin and user.t_id== m_adm.from_user.id)
        chek = (await session.execute(stmt)).scalar()
        
        if chek ==0:
            n_adm = user(name = m_adm.from_user.full_name,
                         t_id = m_adm.from_user.id,
                         role = admin,
                         note = False)
            session.add(n_adm)
            await session.commit()
            await session.close()
        else:
            print("Alredy in use")
            await m_adm.answer('Already in base')
        

@router.message(Command('not'))
async def adm(m_not:Message):
    async with async_session() as session:
        
        
        chek = (await session.execute(select(func.count(user.id).filter(user.role == 'user').filter(user.t_id == m_not.from_user.id)))).scalar()

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
            await m_not.answer('Already in base')
        await session.commit()
        await session.close()

@router.message(Command('get_users'))
async def test_notes(test_not:Message):
    async with async_session() as session:
       users = (await session.scalars(select(user.t_id).where(user.note == True))).all()
       print(users)
    try:
        print(' '.join(users))
        test_not.answer(text= users)
        for i in users:
            print(i)
            test_not.answer(text= str(i))
    except Exception as ex:
        print(ex)
    