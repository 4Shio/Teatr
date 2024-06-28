from typing import Any
from sqlalchemy import URL,create_engine,text,Insert,MetaData,Table,Column,String,values,Integer,select,ForeignKey,ScalarResult
from sqlalchemy.orm import Session,sessionmaker,DeclarativeBase,Mapped,mapped_column,relationship
from config import *
from datetime import*


engine = create_engine(url=url,echo=False,
pool_size=5,
max_overflow=10,
)
session = Session(engine)
metadata = MetaData()
class Base(DeclarativeBase):
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
    


Base.metadata.create_all(engine)