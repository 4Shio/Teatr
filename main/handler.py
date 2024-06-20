from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from base import *
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
from datetime import *
from aiogram.fsm.state import StatesGroup, State

router = Router()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row],one_time_keyboard = True)

remove_key = ReplyKeyboardRemove()

def make_str(text_str):
    return   ' '.join(str(i) for i in text_str )
def make_more_str(text_str):
      return '\n'.join('  '.join(str(i) for i in v) for v in text_str)



with session as session:

    query = select(Speki.name, Speki.date, Speki.time, Speki.info)
    @router.message(Command("start"))
    async def start(message:Message):
                await message.answer(text='Приветсвую - это неофициальный бот музыкального театра для просмотра расписания',reply_markup=make_row_keyboard(["Расписание","Аналитика"]))

    @router.message(F.text == 'Расписание')
    async def get_all(message_get_all:Message):
           await message_get_all.answer(text= make_more_str(session.query(
                  Speki.name,
                  Speki.date,
                  Speki.time,
                  Speki.info).all()))

 
    
    



