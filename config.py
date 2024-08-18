import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
load_dotenv()
url = os.getenv('url')
tg_token = os.getenv('token')

class Base(DeclarativeBase):
    pass
engine  = create_async_engine(url)

async_session = async_sessionmaker(engine)

meta_data = MetaData()
async def init_models():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)