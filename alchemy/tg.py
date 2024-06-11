import asyncio
from aiogram import *
from aiogram.filters import Command 
from aiogram.types import *
from aiogram.utils.keyboard import ReplyKeyboardBuilder

bot = Bot(token='6426552218:AAEAcGWJ69_D3lZB_Ln6v5GRZlULOUR-3V0')
dp = Dispatcher()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


remove_key = ReplyKeyboardRemove()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет от бота", reply_markup=make_row_keyboard(["View", "LAfterT","analys","Next"] ))

@dp.message(F.text == "View")
async def view(message: types.Message):
    pass




