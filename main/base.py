from sqlalchemy import URL,create_engine,text,Insert,MetaData,Table,Column,String,values,Integer,select,ForeignKey
from sqlalchemy.orm import Session,sessionmaker,DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
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
    date:Mapped[str]
    time:Mapped[str]
    info:Mapped[str]

    #addresses: Mapped[List["Address"]] = relationship(
    #    back_populates="Speki",cascade="all, delete-orphan"
    #)

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, name={self.name!r}, date={self.date!r}, time={self.time!r}, info={self.info!r})"
    
class analys(Base):
    __tablename__ = "analys"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    quantity:Mapped[int]


Base.metadata.create_all(engine)