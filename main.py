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


async def main() -> None:

    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)    

    engine = create_async_engine(url=url)
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)
    #Thread(target=update,daemon=True).start()
    while True:
        task0 = asyncio.create_task(engine)
        task1 = asyncio.create_task(update())
        task2 = asyncio.create_task(dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()))
        await task0
        await task1
        await task2
    #try:
    #    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    #except Exception as ex_:
    #    print("Error polling -> ", ex_)
    

if __name__ == "__main__":
    asyncio.run(main())