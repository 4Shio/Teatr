import psycopg2
from sqlalchemy import create_engine
try:
    engine = create_engine('postgresql+psycopg2://admin:root@78.36.44.30:5432/test')
    engine.connect()
    print('Connection Success')
   
except Exception as ex:
    print(ex)
  