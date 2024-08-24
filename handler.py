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
now = datetime.now()

router = Router()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row],one_time_keyboard = True)

remove_key = ReplyKeyboardRemove()

def make_str(text_str):
    return   ' '.join(str(i) for i in text_str )

def make_more_str(text_str):
      return '\n'.join('  '.join(str(i) for i in v) for v in text_str)




    
@router.message(Command("start"))
async def start(message:Message):
                await message.answer(text='Приветсвую - это неофициальный бот музыкального театра для просмотра расписания',reply_markup=make_row_keyboard(["Все следующие","Следующий"]))


@router.message(F.text == 'Все следующие')
async def get_all(message_get_all:Message):
    async with async_session() as session:
        now = datetime.now()
        stmt = select(Speki.message_text).where(Speki.date >now).order_by(Speki.date)
        result =await session.execute(stmt)
        await message_get_all.answer(text= make_more_str(result.all()))
        await session.close()
        
        
@router.message(F.text == 'Следующий')
async def get_all(message_get_one:Message):
    async with async_session() as session:
        now = datetime.now()
        stmt = select(Speki.message_text).where(Speki.date >now).order_by(Speki.date)
        result =await session.scalar(stmt)
        await message_get_one.answer(text= result)
        await session.close()
   

@router.message(Command('op'))
async def adm(m_adm:Message):
    async with async_session() as session:
        admin = 'Admin'
        n_adm = user(name = m_adm.from_user.full_name,
                     t_id = m_adm.from_user.id,
                     role = admin)
        session.add(n_adm)
        await session.commit()
        await session.close()

