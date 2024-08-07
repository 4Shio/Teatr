import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import tg_token,init_models,engine
from handler import router
from update import update


async def main():
    bot = Bot(tg_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router) 
    
    print(engine)
    task01 = asyncio.create_task(init_models())
    task0 = asyncio.create_task(dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()))
    task1 = asyncio.create_task(update())
    await task01
    await task0
    await task1

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        print('Closing')
        
    