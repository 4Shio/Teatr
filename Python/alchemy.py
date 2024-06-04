from sqlalchemy import URL,create_engine,text,Insert,MetaData,Table,Column,String,values,Integer,select
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from bs4 import BeautifulSoup
import requests
from datetime import*

engine = create_engine("postgresql+psycopg2://admin:root@78.36.44.30:5432/test",echo=False,
pool_size=5,
max_overflow=10,
)
meta_data = MetaData()


test_table = Table(
    'test',
    meta_data,
    Column('id',Integer,primary_key=True),
    Column('name',String),
    Column('date',String),
    Column('time',String),
    Column('info',String)
)
analys_table=Table(
    'analys',
    meta_data,
    Column('id',Integer,primary_key=True),
    Column('name',String),
    Column('date',String),
)


