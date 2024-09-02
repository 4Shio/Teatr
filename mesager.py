from base import user,Speki
from config import async_session

from datetime import *
from sqlalchemy import select,func


async def mesager():
    while True:
        try:
            async with async_session() as session:
                stmt = select(Speki.date).order_by(Speki.date)
                first_date = await session.scalar(stmt)
                time_untill = first_date  - datetime.now()
                if datetime.now().day == (first_date - timedelta(days= 1)):
                    print()
        except Exception as ex:
            print(ex)
            
            
            
            
            
            
            