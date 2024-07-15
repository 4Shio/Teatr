from datetime import *
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Mapped,mapped_column
from base import *
from config import *
from handler import *
from update import update
from threading import Thread

bot = Bot(token)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router) 



loop = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        asyncio.ensure_future(update())
        asyncio.ensure_future(dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print('Closing loop')
        loop.close()
    