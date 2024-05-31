
import psycopg2
from sqlalchemy import create_engine,MetaData,Table,String,Integer,Column,DateTime,Boolean,Text
import datetime
now =datetime.datetime.now
try:
    engine = create_engine('postgresql+psycopg2://admin:root@78.36.44.30:5432/test')
    engine.connect()
    print('Connection Success')
   
except Exception as ex:
    print(ex)
  
metadata = MetaData()

blog = Table('blog', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('post_title', String(200), nullable=False),
    Column('post_slug', String(200),  nullable=False),
    Column('content', Text(), nullable=False),
    Column('published', Boolean(), default=False),
    Column('created_on', DateTime(), default=now),
    Column('updated_on', DateTime(), default=now, onupdate=now)
)