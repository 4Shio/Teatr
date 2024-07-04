from typing import Any
from sqlalchemy import URL,create_engine,text,Insert,MetaData,Table,Column,String,values,Integer,select,ForeignKey,ScalarResult
from sqlalchemy.orm import Session,sessionmaker,DeclarativeBase,Mapped,mapped_column,relationship

from config import *
from datetime import*
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, AsyncSession, create_async_engine
import asyncio

#async_engine = create_async_engine(url= asyncurl,echo = False)
engine = create_async_engine(url= asyncurl,echo = False)
async_session = async_sessionmaker(engine)
#async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#session = Session(engine)
metadata = MetaData()


class Base(AsyncAttrs,DeclarativeBase):
    pass

class Speki(Base):
    __tablename__ = "Speki"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    date:Mapped[datetime]
    info:Mapped[str]
    weekday:Mapped[str]
    message_text:Mapped[str]
 

    def __repr__(self) -> str:
        return f"( {self.name!r} {self.date!r} {self.info!r}  {self.weekday!r})"
    



#Base.metadata.create_all(engine)
async def init_models():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())